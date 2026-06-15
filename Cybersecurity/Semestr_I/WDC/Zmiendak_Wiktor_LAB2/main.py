from __future__ import annotations

import math
import secrets
from pathlib import Path
from typing import List, Tuple

P_VALUE_THRESHOLD = 0.01
PRIME_BITS = 64


def read_message(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def text_to_bits(text: str) -> List[int]:
    data = text.encode("utf-8")
    return [(byte >> shift) & 1 for byte in data for shift in range(7, -1, -1)]


def bits_to_text(bits: List[int]) -> str:
    if len(bits) % 8 != 0:
        raise ValueError("Liczba bitow musi byc podzielna przez 8")

    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i : i + 8]:
            byte = (byte << 1) | bit
        data.append(byte)
    return data.decode("utf-8")


def xor_bits(a: List[int], b: List[int]) -> List[int]:
    if len(a) != len(b):
        raise ValueError("Ciagi bitow musza miec taka sama dlugosc")
    return [x ^ y for x, y in zip(a, b)]


def is_probable_prime(n: int, rounds: int = 20) -> bool:
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    small_primes = [3, 5, 7, 11, 13, 17, 19, 23, 29]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False

    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(rounds):
        a = secrets.randbelow(n - 3) + 2
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True


def generate_blum_prime(bits: int) -> int:
    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1)) | 1
        candidate = (candidate & ~0b11) | 0b11
        if is_probable_prime(candidate):
            return candidate


def generate_coprime_seed(n: int) -> int:
    while True:
        seed = secrets.randbelow(n - 2) + 2
        if math.gcd(seed, n) == 1:
            return seed


def blum_blum_shub(
    bit_count: int, prime_bits: int = PRIME_BITS
) -> Tuple[List[int], int, int, int, int]:
    p = generate_blum_prime(prime_bits)
    q = generate_blum_prime(prime_bits)
    while q == p:
        q = generate_blum_prime(prime_bits)

    n = p * q
    seed = generate_coprime_seed(n)

    x = pow(seed, 2, n)
    key_bits: List[int] = []
    for _ in range(bit_count):
        x = pow(x, 2, n)
        key_bits.append(x % 2)

    return key_bits, p, q, n, seed


def monobit_test(bits: List[int]) -> Tuple[bool, float]:
    n = len(bits)
    if n == 0:
        return False, 0.0

    s_n = sum(1 if bit == 1 else -1 for bit in bits)
    s_obs = abs(s_n) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value >= P_VALUE_THRESHOLD, p_value


def runs_test(bits: List[int]) -> Tuple[bool, float, str]:
    n = len(bits)
    if n == 0:
        return False, 0.0, "Pusty ciag bitow"

    pi = sum(bits) / n
    tau = 2 / math.sqrt(n)
    if abs(pi - 0.5) >= tau:
        return False, 0.0, "Warunek wstepny runs nie jest spelniony"

    runs_count = 1 + sum(1 for i in range(1, n) if bits[i] != bits[i - 1])
    numerator = abs(runs_count - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    p_value = math.erfc(numerator / denominator)
    return p_value >= P_VALUE_THRESHOLD, p_value, "OK"


def bits_to_string(bits: List[int]) -> str:
    return "".join(str(bit) for bit in bits)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_file = base_dir / "secret_message.txt"
    encrypted_file = base_dir / "zaszyfrowane_bity.txt"
    decrypted_file = base_dir / "odszyfrowana_wiadomosc.txt"

    message = read_message(input_file)
    message_bits = text_to_bits(message)

    key_bits, p, q, n, seed = blum_blum_shub(len(message_bits))

    mono_pass, mono_p = monobit_test(key_bits)
    runs_pass, runs_p, runs_note = runs_test(key_bits)

    encrypted_bits = xor_bits(message_bits, key_bits)
    decrypted_bits = xor_bits(encrypted_bits, key_bits)
    decrypted_message = bits_to_text(decrypted_bits)

    encrypted_file.write_text(bits_to_string(encrypted_bits), encoding="utf-8")
    decrypted_file.write_text(decrypted_message, encoding="utf-8")

    print("=== Parametry BBS ===")
    print(f"p = {p}")
    print(f"q = {q}")
    print(f"n = {n}")
    print(f"seed = {seed}")

    print("\n=== Testy NIST ===")
    print(f"Monobit: {'PASS' if mono_pass else 'FAIL'}, p-value = {mono_p:.6f}")
    print(
        f"Runs: {'PASS' if runs_pass else 'FAIL'}, p-value = {runs_p:.6f}, info = {runs_note}"
    )

    print("\n=== Wynik ===")
    print(f"Dlugosc wiadomosci: {len(message)} znakow")
    print(f"Dlugosc bitowa: {len(message_bits)} bitow")
    print(f"Plik szyfrogramu: {encrypted_file.name}")
    print(f"Plik odszyfrowanej wiadomosci: {decrypted_file.name}")
    print(f"Zgodnosc oryginalu i odszyfrowania: {message == decrypted_message}")


if __name__ == "__main__":
    main()
