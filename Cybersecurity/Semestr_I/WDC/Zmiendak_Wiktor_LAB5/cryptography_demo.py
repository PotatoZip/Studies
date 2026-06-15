from __future__ import annotations

import argparse
import os
import time
from pathlib import Path

from cryptography.hazmat.primitives import hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from crypto_task_utils import (
    chunk_data,
    load_input_file,
    pack_blocks,
    print_section,
    unpack_blocks,
    write_text,
)


def rsa_limit_oaep(public_key: rsa.RSAPublicKey) -> int:
    # Maksymalny rozmiar bloku dla RSA-OAEP przy SHA-256
    return public_key.key_size // 8 - 2 * hashes.SHA256().digest_size - 2


def rsa_limit_pkcs1(public_key: rsa.RSAPublicKey) -> int:
    # Maksymalny rozmiar bloku dla RSA-PKCS1v15
    return public_key.key_size // 8 - 11


def rsa_round_trip(
    data: bytes,
    private_key: rsa.RSAPrivateKey,
    output_dir: Path,
    name: str,
    padding_obj,
    limit: int,
) -> None:
    # Szyfruje dane po kawałku i sprawdza poprawność odszyfrowania
    public_key = private_key.public_key()
    encrypted = [
        public_key.encrypt(chunk, padding_obj) for chunk in chunk_data(data, limit)
    ]
    enc_path = output_dir / f"{name}.enc.bin"
    dec_path = output_dir / f"{name}.dec.txt"
    enc_path.write_bytes(pack_blocks(encrypted))
    decrypted = [
        private_key.decrypt(block, padding_obj)
        for block in unpack_blocks(enc_path.read_bytes())
    ]
    write_text(dec_path, b"".join(decrypted))
    print(
        f" {name.replace('_', '-').upper()} round-trip: {b''.join(decrypted) == data}"
    )


def symmetric(data: bytes, output_dir: Path) -> None:
    # Dwa algorytmy szyfrowania symetrycznego
    print_section("1) Symetryczne szyfrowanie i odszyfrowanie")
    # AES-256-CBC - wymaga dopełnienia PKCS7
    key, iv = os.urandom(32), os.urandom(16)
    padder = sym_padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    encryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    (output_dir / "aes_cbc.enc.bin").write_bytes(iv + ciphertext)
    decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    unpadder = sym_padding.PKCS7(128).unpadder()
    plain = (
        unpadder.update(decryptor.update(ciphertext) + decryptor.finalize())
        + unpadder.finalize()
    )
    write_text(output_dir / "aes_cbc.dec.txt", plain)
    print(f"AES-256-CBC round-trip: {plain == data}")

    # AES-256
    key, nonce = os.urandom(32), os.urandom(12)
    ciphertext = AESGCM(key).encrypt(nonce, data, None)
    (output_dir / "aes_gcm.enc.bin").write_bytes(nonce + ciphertext)
    plain = AESGCM(key).decrypt(nonce, ciphertext, None)
    write_text(output_dir / "aes_gcm.dec.txt", plain)
    print(f" AES-256-GCM round-trip: {plain == data}")


def asymmetric(data: bytes, private_key: rsa.RSAPrivateKey, output_dir: Path) -> None:
    # Dwa algorytmy szyfrowania asymetrycznego
    print_section("2) Asymetryczne szyfrowanie i odszyfrowanie")
    oaep = asym_padding.OAEP(
        mgf=asym_padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None
    )
    pkcs1 = asym_padding.PKCS1v15()
    rsa_round_trip(
        data,
        private_key,
        output_dir,
        "rsa_oaep",
        oaep,
        rsa_limit_oaep(private_key.public_key()),
    )
    rsa_round_trip(
        data,
        private_key,
        output_dir,
        "rsa_pkcs1v15",
        pkcs1,
        rsa_limit_pkcs1(private_key.public_key()),
    )


def hashes_and_signature(
    data: bytes, private_key: rsa.RSAPrivateKey, output_dir: Path
) -> None:
    # Hashe oraz podpis cyfrowy
    print_section("3) Funkcje skrótu")
    sha256 = hashes.Hash(hashes.SHA256())
    sha256.update(data)
    sha256_hex = sha256.finalize().hex()
    (output_dir / "sha256.txt").write_text(sha256_hex, encoding="utf-8")
    print(f" SHA-256 digest: {sha256_hex[:32]}...")

    sha512 = hashes.Hash(hashes.SHA512())
    sha512.update(data)
    sha512_hex = sha512.finalize().hex()
    (output_dir / "sha512.txt").write_text(sha512_hex, encoding="utf-8")
    print(f" SHA-512 digest: {sha512_hex[:32]}...")

    print_section("4) Podpis cyfrowy")
    # RSA-PSS - podpis kluczem prywatnym i weryfikacja kluczem publicznym
    public_key = private_key.public_key()
    signature = private_key.sign(
        data,
        asym_padding.PSS(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            salt_length=asym_padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    public_key.verify(
        signature,
        data,
        asym_padding.PSS(
            mgf=asym_padding.MGF1(hashes.SHA256()),
            salt_length=asym_padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    (output_dir / "signature.bin").write_bytes(signature)
    print(" RSA-PSS signature verification: True")


def run_demo(input_file: Path) -> None:
    # Główna funkcja uruchamiająca
    data = load_input_file(input_file)
    output_dir = input_file.parent / "outputs" / "cryptography"
    output_dir.mkdir(parents=True, exist_ok=True)
    print("\n" + "=" * 60)
    print("LIBRARY 2: cryptography")
    print("=" * 60)
    print(f"Plik wejściowy: {input_file.name}")
    print(f"Rozmiar danych: {len(data)} bytes")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    started = time.perf_counter()
    symmetric(data, output_dir)
    asymmetric(data, private_key, output_dir)
    hashes_and_signature(data, private_key, output_dir)
    print(f"Łączny czas demonstracji: {time.perf_counter() - started:.4f} s")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo cryptography na danych z pliku")
    parser.add_argument(
        "input_file",
        nargs="?",
        default="sample_input.txt",
        help="Plik wejściowy do demonstracji",
    )
    return parser.parse_args()


if __name__ == "__main__":
    run_demo(Path(parse_args().input_file))
