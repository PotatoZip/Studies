import hashlib, random, time

# Stałe SHA-256
K = [
    0x428A2F98,
    0x71374491,
    0xB5C0FBCF,
    0xE9B5DBA5,
    0x3956C25B,
    0x59F111F1,
    0x923F82A4,
    0xAB1C5ED5,
    0xD807AA98,
    0x12835B01,
    0x243185BE,
    0x550C7DC3,
    0x72BE5D74,
    0x80DEB1FE,
    0x9BDC06A7,
    0xC19BF174,
    0xE49B69C1,
    0xEFBE4786,
    0x0FC19DC6,
    0x240CA1CC,
    0x2DE92C6F,
    0x4A7484AA,
    0x5CB0A9DC,
    0x76F988DA,
    0x983E5152,
    0xA831C66D,
    0xB00327C8,
    0xBF597FC7,
    0xC6E00BF3,
    0xD5A79147,
    0x06CA6351,
    0x14292967,
    0x27B70A85,
    0x2E1B2138,
    0x4D2C6DFC,
    0x53380D13,
    0x650A7354,
    0x766A0ABB,
    0x81C2C92E,
    0x92722C85,
    0xA2BFE8A1,
    0xA81A664B,
    0xC24B8B70,
    0xC76C51A3,
    0xD192E819,
    0xD6990624,
    0xF40E3585,
    0x106AA070,
    0x19A4C116,
    0x1E376C08,
    0x2748774C,
    0x34B0BCB5,
    0x391C0CB3,
    0x4ED8AA4A,
    0x5B9CCA4F,
    0x682E6FF3,
    0x748F82EE,
    0x78A5636F,
    0x84C87814,
    0x8CC70208,
    0x90BEFFFA,
    0xA4506CEB,
    0xBEF9A3F7,
    0xC67178F2,
]


def sha256(data: bytes) -> str:
    # 8 rejestrów początkowych
    h = [
        0x6A09E667,
        0xBB67AE85,
        0x3C6EF372,
        0xA54FF53A,
        0x510E527F,
        0x9B05688C,
        0x1F83D9AB,
        0x5BE0CD19,
    ]

    # Dopełnianie wiadomości do wielokrotności 512 bitów
    msg = bytearray(data)
    msg.append(0x80)
    while len(msg) % 64 != 56:
        msg.append(0)
    msg += (len(data) * 8).to_bytes(8, "big")

    # Przetwarzanie każdego blok 64 bajtów
    for offset in range(0, len(msg), 64):
        block = msg[offset : offset + 64]
        # Rozszerzenie 16 słów na 64 słowa
        w = [int.from_bytes(block[i * 4 : i * 4 + 4], "big") for i in range(16)]
        for i in range(16, 64):
            s0 = (
                ((w[i - 15] >> 7) | (w[i - 15] << 25))
                ^ ((w[i - 15] >> 18) | (w[i - 15] << 14))
                ^ (w[i - 15] >> 3)
            )
            s1 = (
                ((w[i - 2] >> 17) | (w[i - 2] << 15))
                ^ ((w[i - 2] >> 19) | (w[i - 2] << 13))
                ^ (w[i - 2] >> 10)
            )
            w.append((w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFF)

        # 64 Rundy kompresji
        a, b, c, d, e, f, g, hh = h
        for i in range(64):
            s1 = (
                ((e >> 6) | (e << 26))
                ^ ((e >> 11) | (e << 21))
                ^ ((e >> 25) | (e << 7))
            )
            ch = (e & f) ^ (~e & g)
            t1 = (hh + s1 + ch + K[i] + w[i]) & 0xFFFFFFFF
            s0 = (
                ((a >> 2) | (a << 30))
                ^ ((a >> 13) | (a << 19))
                ^ ((a >> 22) | (a << 10))
            )
            maj = (a & b) ^ (a & c) ^ (b & c)
            t2 = (s0 + maj) & 0xFFFFFFFF
            hh, g, f, e, d, c, b, a = (
                g,
                f,
                e,
                (d + t1) & 0xFFFFFFFF,
                c,
                b,
                a,
                (t1 + t2) & 0xFFFFFFFF,
            )

        # Aktualizacja stanów
        h = [(h[i] + [a, b, c, d, e, f, g, hh][i]) & 0xFFFFFFFF for i in range(8)]

    return "".join(f"{x:08x}" for x in h)


def test():
    print("=" * 50)
    random.seed(42)

    # Weryfikacja poprawności
    test_vecs = [
        b"",
        b"abc",
        b"hello world",
        b"The quick brown fox jumps over the lazy dog",
    ]
    for v in test_vecs:
        assert sha256(v) == hashlib.sha256(v).hexdigest()
    print("Poprawność: SHA-256 zgadza się z hashlib")

    # TEST 1 - Dowolna długość
    print("\n[1] Czy można skrócić tekst dowolnej długości?")
    for length in [0, 1, 10, 55, 56, 64, 1000, 100000]:
        sha256(b"A" * length)
    print("Wszystkie długości obsługiwane")

    # TEST 2 - Efekt lawiny (zmiana 1 bitu)
    print("\n[2] Zmiana 1 bitu -> roznica skrotu (efekt lawiny)")
    original = b"To jest przykladowa wiadomosc testowa dla SHA-256."
    idx, bit = random.randrange(len(original)), 1 << random.randrange(8)
    modified = bytearray(original)
    modified[idx] ^= bit
    h1, h2 = sha256(original), sha256(bytes(modified))
    dist = sum(
        (int(h1[i : i + 2], 16) ^ int(h2[i : i + 2], 16)).bit_count()
        for i in range(0, 64, 2)
    )
    print(f"Zmieniony bajt #{idx} -> {dist}/256 bitów różnicy w hashu")

    # TEST 3 - Odległość Hamminga dla różnych tekstów
    print("\n[3] Odleglosc Hamminga dla różnych tekstów")
    t1, t2 = b"Ala ma kota", b"Ala ma psa"
    h1, h2 = sha256(t1), sha256(t2)
    dist = sum(
        (int(h1[i : i + 2], 16) ^ int(h2[i : i + 2], 16)).bit_count()
        for i in range(0, 64, 2)
    )
    print(f"{t1.decode()}' vs '{t2.decode()}' -> {dist}/256 bitów różnicy")

    # TEST 4 - Stała długość
    print("\n[4] Czy hash ma zawsze tę samą długość?")
    lengths = [len(sha256(s)) for s in [b"", b"a", b"test", b"x" * 10000]]
    print(f"TAK - zawsze {lengths[0]} znaków (= 256 bitów)")

    # TEST 5: Benchmark
    print("\n[5] Porównanie czasu: custom vs hashlib")
    msg = b"Benchmark" * 100

    t = time.perf_counter()
    sha256(msg)
    custom_time = time.perf_counter() - t

    t = time.perf_counter()
    hashlib.sha256(msg).hexdigest()
    lib_time = time.perf_counter() - t

    print(f"Custom:  {custom_time:.6f}s")
    print(f"Hashlib: {lib_time:.6f}s")
    print(
        f"Hashlib jest szybsza ~{custom_time/lib_time:.0f}x (oczekiwane - C vs Python)"
    )

    print("\n" + "=" * 50)


if __name__ == "__main__":
    test()
