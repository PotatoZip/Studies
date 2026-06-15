from __future__ import annotations

import argparse
import csv
import json
import math
import random
import time
from pathlib import Path

# Zestaw alfabetów do wyboru
ALPHABETS = {
    "26": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "64": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 .",
    "ascii": "".join(chr(i) for i in range(128)),
}


# Podział tekstu na bloki o określonej długości
def chunks(text: str, size: int):
    return [text[i : i + size] for i in range(0, len(text), size)]


# Zamiana bloku tekstu na liczbę całkowitą
def block_to_int(block: str, base: int, c2i: dict[str, int]) -> int:
    x = 0
    for ch in block:
        x = x * base + c2i[ch]
    return x


# Zamiana liczby całkowitej z powrotem na blok tekstu
def int_to_block(x: int, length: int, base: int, i2c: dict[int, str]) -> str:
    out = []
    for _ in range(length):
        out.append(i2c[x % base])
        x //= base
    out.reverse()
    return "".join(out)


# Budowanie mapowania znak <-> indeks dla wybranego alfabetu
def codec(alphabet: str):
    c2i = {c: i for i, c in enumerate(alphabet)}
    i2c = {i: c for i, c in enumerate(alphabet)}
    return c2i, i2c


# Sprawdzenie, czy tekst zawiera tylko znaki z wybranego alfabetu
def check_text_uses_alphabet(text: str, alphabet: str) -> None:
    bad = sorted({ch for ch in text if ch not in alphabet})
    if bad:
        preview = " ".join(repr(ch) for ch in bad[:5])
        raise ValueError(f"Niedozwolone znaki dla alfabetu: {preview}")


# Test Miller-Rabina, sprawdzający czy liczba jest prawdopodobnie pierwsza
def is_probable_prime(n: int, rounds: int = 40) -> bool:
    if n < 2:
        return False

    small = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False

    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True


# Generowanie liczby pierwszej o określonej liczbie bitów, która jest względnie pierwsza do e
def prime(bits: int, e: int = 65537) -> int:
    while True:
        p = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_probable_prime(p) and math.gcd(p - 1, e) == 1:
            return p


# Generowanie klucza RSA
def rsa_key(bits: int = 768, e: int = 65537):
    if bits < 768:
        raise ValueError("Klucz RSA musi miec >= 768 bitow")

    a = bits // 2
    b = bits - a
    while True:
        p = prime(a, e)
        q = prime(b, e)
        if p == q:
            continue
        n = p * q
        if n.bit_length() < bits:
            continue
        phi = (p - 1) * (q - 1)
        if math.gcd(e, phi) != 1:
            continue
        d = pow(e, -1, phi)
        return {"p": p, "q": q, "n": n, "e": e, "d": d}


# Uruchomienie RSA i faktoryzacji z argumentami z linii poleceń
def run_rsa(
    input_file: Path, alphabet_key: str, key_bits: int, block_size: int, out: Path
):
    alphabet = ALPHABETS[alphabet_key]
    base = len(alphabet)
    c2i, i2c = codec(alphabet)

    text = input_file.read_text(encoding="utf-8")
    check_text_uses_alphabet(text, alphabet)

    raw_blocks = chunks(text, block_size)
    pad_char = alphabet[0]
    padded = [b.ljust(block_size, pad_char) for b in raw_blocks]
    values = [block_to_int(b, base, c2i) for b in padded]

    # Generowanie klucza RSA
    key = rsa_key(bits=key_bits)

    encrypted = []
    for m in values:
        if m >= key["n"]:
            raise ValueError("Blok musi spelnic warunek m < n")
        encrypted.append(pow(m, key["e"], key["n"]))

    # Odszyfrowanie i sprawdzenie poprawności
    decrypted_values = [pow(c, key["d"], key["n"]) for c in encrypted]
    decrypted_padded = "".join(
        int_to_block(v, block_size, base, i2c) for v in decrypted_values
    )
    decrypted = decrypted_padded[: len(text)]

    # Sprawdzenie, czy odszyfrowane bloki są identyczne z oryginalnymi
    decrypted_blocks = chunks(decrypted, block_size)
    checks = []
    for i, ob in enumerate(raw_blocks):
        db = decrypted_blocks[i] if i < len(decrypted_blocks) else ""
        checks.append((i, ob, db, ob == db))

    out.mkdir(parents=True, exist_ok=True)
    (out / "encrypted_blocks.txt").write_text(
        "\n".join(map(str, encrypted)), encoding="utf-8"
    )
    (out / "decrypted_message.txt").write_text(decrypted, encoding="utf-8")
    (out / "block_check.txt").write_text(
        "\n".join(
            f"blok={i:03d} status={'OK' if ok else 'FAIL'} oryg={ob!r} dec={db!r}"
            for i, ob, db, ok in checks
        ),
        encoding="utf-8",
    )

    summary = {
        "alphabet": alphabet_key,
        "alphabet_size": base,
        "block_size": block_size,
        "message_length": len(text),
        "num_blocks": len(raw_blocks),
        "key_bits": key["n"].bit_length(),
        "e": key["e"],
        "n": key["n"],
        "all_blocks_equal": all(ok for _, _, _, ok in checks),
    }
    (out / "rsa_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    return summary


# Jedna proba faktoryzacji metoda Pollarda Rho
def pollard_rho_once(n: int, max_iters: int = 2_000_000):
    if n % 2 == 0:
        return 2, 1

    x = random.randrange(2, n - 1)
    y = x
    c = random.randrange(1, n - 1)
    d, it = 1, 0

    while d == 1 and it < max_iters:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = math.gcd(abs(x - y), n)
        it += 1

    if d in (1, n):
        return None, it
    return d, it


# Powtarza Pollarda Rho kilka razy i zwraca najlepszy wynik.
def factor_pollard_rho(n: int, attempts: int = 14):
    if n % 2 == 0:
        return 2, n // 2, 1, True

    total = 0
    for _ in range(attempts):
        d, it = pollard_rho_once(n)
        total += it
        if d is None:
            continue
        p, q = d, n // d
        if p * q == n:
            return min(p, q), max(p, q), total, True
    return None, None, total, False


# Tworzy liczbe zlozona z dwoch liczb pierwszych o zadanej dlugosci.
def semiprime(bits: int):
    a = bits // 2
    b = bits - a
    while True:
        p = prime(a, e=3)
        q = prime(b, e=3)
        if p != q and (p * q).bit_length() == bits:
            return p * q, min(p, q), max(p, q)


# Oblicza wspolczynnik dopasowania R^2 dla modelu.
def r2(y, yhat):
    ym = sum(y) / len(y)
    ss_tot = sum((v - ym) ** 2 for v in y)
    ss_res = sum((a - b) ** 2 for a, b in zip(y, yhat))
    return 1.0 if ss_tot == 0 else 1.0 - ss_res / ss_tot


# Dopasowuje modele liniowy, potegowy i wykladniczy do danych
def fit_models(bits, times_sec):
    import numpy as np

    x = np.array(bits, dtype=float)
    y = np.array(times_sec, dtype=float)
    y_safe = np.clip(y, 1e-12, None)

    lin = np.polyfit(x, y, 1)
    lin_pred = lambda z: float(lin[0] * z + lin[1])

    pw = np.polyfit(np.log(x), np.log(y_safe), 1)
    a_pw, b_pw = float(math.exp(pw[1])), float(pw[0])
    pw_pred = lambda z: float(a_pw * (z**b_pw))

    ex = np.polyfit(x, np.log(y_safe), 1)
    a_ex, b_ex = float(math.exp(ex[1])), float(ex[0])
    ex_pred = lambda z: float(a_ex * math.exp(b_ex * z))

    models = {
        "linear": {
            "params": {"a": float(lin[0]), "b": float(lin[1])},
            "predict": lin_pred,
        },
        "power": {"params": {"a": a_pw, "b": b_pw}, "predict": pw_pred},
        "exponential": {"params": {"a": a_ex, "b": b_ex}, "predict": ex_pred},
    }
    for name in models:
        yhat = [models[name]["predict"](float(v)) for v in x]
        models[name]["r2"] = float(r2(y, yhat))
    return models


# Uruchamia benchmark faktoryzacji i zapisuje wyniki do plikow
def run_factor(sizes: list[int], out: Path):
    import matplotlib.pyplot as plt
    import numpy as np

    rows = []
    for bits in sizes:
        n, p_true, q_true = semiprime(bits)
        t0 = time.perf_counter()
        p, q, iters, ok = factor_pollard_rho(n)
        dt = time.perf_counter() - t0
        ok = ok and (p, q) == (p_true, q_true)
        rows.append(
            {
                "bits": bits,
                "n": n,
                "method": "Pollard Rho",
                "seconds": dt,
                "iterations": iters,
                "success": ok,
                "p_found": p,
                "q_found": q,
            }
        )

    out.mkdir(parents=True, exist_ok=True)

    # Zapis wyników do CSV
    with (out / "factorization_results.csv").open(
        "w", encoding="utf-8", newline=""
    ) as f:
        w = csv.writer(f)
        w.writerow(
            [
                "bits",
                "n",
                "method",
                "seconds",
                "iterations",
                "success",
                "p_found",
                "q_found",
            ]
        )
        for r in rows:
            w.writerow(
                [
                    r["bits"],
                    r["n"],
                    r["method"],
                    f"{r['seconds']:.9f}",
                    r["iterations"],
                    r["success"],
                    r["p_found"] if r["p_found"] else "",
                    r["q_found"] if r["q_found"] else "",
                ]
            )

    good = [r for r in rows if r["success"]]
    if len(good) < 3:
        raise RuntimeError("Za malo udanych punktow do dopasowania")

    bits = [r["bits"] for r in good]
    times = [r["seconds"] for r in good]
    models = fit_models(bits, times)
    best = max(models, key=lambda k: models[k]["r2"])
    extrap = {b: models[best]["predict"](b) for b in [96, 128, 256]}

    x_line = np.linspace(min(bits), max(bits), 300)
    plt.figure(figsize=(10, 6))
    plt.scatter(bits, times, color="#005f73", s=55, label="pomiary")
    for name, color in [
        ("linear", "#ca6702"),
        ("power", "#bb3e03"),
        ("exponential", "#9b2226"),
    ]:
        plt.plot(
            x_line,
            [models[name]["predict"](float(x)) for x in x_line],
            color=color,
            label=f"{name} (R^2={models[name]['r2']:.4f})",
        )
    plt.xlabel("Rozmiar klucza [bity]")
    plt.ylabel("Czas faktoryzacji [s]")
    plt.title("Faktoryzacja RSA")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out / "factorization_plot.png", dpi=160)
    plt.close()

    payload = {
        "results": rows,
        "fits": {
            name: {"params": models[name]["params"], "r2": models[name]["r2"]}
            for name in models
        },
        "best_fit": best,
        "extrapolation_seconds": extrap,
    }
    (out / "factorization_analysis.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    return payload


# Parsuje argumenty z linii polecen dla trybu RSA lub factor
def parse_args():
    p = argparse.ArgumentParser(description="RSA + faktoryzacja")
    sub = p.add_subparsers(dest="cmd", required=True)

    rsa = sub.add_parser("rsa")
    rsa.add_argument("--input", type=Path, required=True)
    rsa.add_argument("--alphabet", choices=list(ALPHABETS), default="ascii")
    rsa.add_argument("--key-bits", type=int, default=768)
    rsa.add_argument("--block-size", type=int, default=10)
    rsa.add_argument("--out", type=Path, default=Path("out"))

    fac = sub.add_parser("factor")
    fac.add_argument(
        "--sizes", nargs="+", type=int, default=[32, 40, 48, 56, 64, 72, 80, 88]
    )
    fac.add_argument("--out", type=Path, default=Path("out"))

    return p.parse_args()


def main():
    args = parse_args()

    if args.cmd == "rsa":
        summary = run_rsa(
            args.input, args.alphabet, args.key_bits, args.block_size, args.out
        )
        print("RSA zakonczone")
        print(json.dumps(summary, indent=2))
    else:
        payload = run_factor(args.sizes, args.out)
        print("Faktoryzacja zakonczona")
        print(
            json.dumps(
                {"best_fit": payload["best_fit"], "fits": payload["fits"]}, indent=2
            )
        )


if __name__ == "__main__":
    main()
