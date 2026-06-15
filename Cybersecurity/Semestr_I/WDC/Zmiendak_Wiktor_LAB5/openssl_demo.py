from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from crypto_task_utils import (
    chunk_data,
    load_input_file,
    pack_blocks,
    print_section,
    unpack_blocks,
    write_text,
)


def run(cmd: list[str], capture_output: bool = False) -> subprocess.CompletedProcess:
    # Wspólny wrapper na wywołania OpenSSL CLI
    try:
        return subprocess.run(cmd, check=True, capture_output=capture_output)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            f"OpenSSL command failed: {' '.join(cmd)}\nexit={exc.returncode}\n{exc.stderr}"
        )


def ensure_openssl_available() -> None:
    # Sprawdza czy polecenie openssl jest dostępne w systemie
    if shutil.which("openssl") is None:
        raise RuntimeError("`openssl` nie jest dostępny w PATH. Zainstaluj OpenSSL.")


def temp_file(data: bytes, suffix: str = ".bin") -> Path:
    # Tworzy tymczasowy plik wejściowy/wyjściowy dla operacji OpenSSL
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    temp_path = Path(path)
    temp_path.write_bytes(data)
    return temp_path


def hexstr(data: bytes) -> str:
    return data.hex()


def rsa_limit_oaep() -> int:
    # Limit bloku dla RSA-OAEP przy RSA-2048 i SHA-256
    return 256 - 2 * 32 - 2


def rsa_limit_pkcs1() -> int:
    # Limit bloku dla RSA-PKCS1v15 przy RSA-2048
    return 256 - 11


def gen_keys(output_dir: Path) -> tuple[Path, Path]:
    # Generuje klucz prywatny i publiczny RSA potrzebne do sekcji asymetrycznej i podpisu
    private_key = output_dir / "private.pem"
    public_key = output_dir / "public.pem"
    run(
        [
            "openssl",
            "genpkey",
            "-algorithm",
            "RSA",
            "-pkeyopt",
            "rsa_keygen_bits:2048",
            "-out",
            str(private_key),
        ]
    )
    run(["openssl", "rsa", "-in", str(private_key), "-pubout", "-out", str(public_key)])
    return private_key, public_key


def symmetric(data: bytes, output_dir: Path) -> None:
    # Dwa algorytmy symetryczne dostępne przez OpenSSL CLI
    print_section("1) Symetryczne szyfrowanie i odszyfrowanie")
    for name, mode in (("aes_cbc", "-aes-256-cbc"), ("aes_ctr", "-aes-256-ctr")):
        key, iv = os.urandom(32), os.urandom(16)
        infile = temp_file(data)
        enc_path = output_dir / f"{name}.enc.bin"
        dec_path = output_dir / f"{name}.dec.txt"
        run(
            [
                "openssl",
                "enc",
                mode,
                "-K",
                hexstr(key),
                "-iv",
                hexstr(iv),
                "-in",
                str(infile),
                "-out",
                str(enc_path),
                "-nosalt",
            ]
        )
        run(
            [
                "openssl",
                "enc",
                "-d",
                mode,
                "-K",
                hexstr(key),
                "-iv",
                hexstr(iv),
                "-in",
                str(enc_path),
                "-out",
                str(dec_path),
                "-nosalt",
            ]
        )
        infile.unlink(missing_ok=True)
        print(
            f" {name.replace('_', '-').upper()} round-trip written to: {enc_path.name} {dec_path.name}"
        )


def rsa_round_trip(
    data: bytes, private_key: Path, public_key: Path, output_dir: Path
) -> None:
    # RSA-OAEP i RSA-PKCS1v15 z dzieleniem danych na bloki
    print_section("2) Asymetryczne szyfrowanie i odszyfrowanie")
    for name, padding_mode, limit in (
        ("rsa_oaep", "oaep", rsa_limit_oaep()),
        ("rsa_pkcs1v15", "pkcs1", rsa_limit_pkcs1()),
    ):
        encrypted_blocks: list[bytes] = []
        for chunk in chunk_data(data, limit):
            chunk_in = temp_file(chunk)
            chunk_out = temp_file(b"")
            run(
                [
                    "openssl",
                    "pkeyutl",
                    "-encrypt",
                    "-inkey",
                    str(public_key),
                    "-pubin",
                    "-pkeyopt",
                    f"rsa_padding_mode:{padding_mode}",
                    *(
                        ["-pkeyopt", "rsa_oaep_md:sha256"]
                        if padding_mode == "oaep"
                        else []
                    ),
                    "-in",
                    str(chunk_in),
                    "-out",
                    str(chunk_out),
                ]
            )
            encrypted_blocks.append(chunk_out.read_bytes())
            chunk_in.unlink(missing_ok=True)
            chunk_out.unlink(missing_ok=True)

        enc_path = output_dir / f"{name}.enc.bin"
        dec_path = output_dir / f"{name}.dec.txt"
        enc_path.write_bytes(pack_blocks(encrypted_blocks))

        decrypted_blocks: list[bytes] = []
        for block in unpack_blocks(enc_path.read_bytes()):
            block_in = temp_file(block)
            block_out = temp_file(b"")
            run(
                [
                    "openssl",
                    "pkeyutl",
                    "-decrypt",
                    "-inkey",
                    str(private_key),
                    "-pkeyopt",
                    f"rsa_padding_mode:{padding_mode}",
                    *(
                        ["-pkeyopt", "rsa_oaep_md:sha256"]
                        if padding_mode == "oaep"
                        else []
                    ),
                    "-in",
                    str(block_in),
                    "-out",
                    str(block_out),
                ]
            )
            decrypted_blocks.append(block_out.read_bytes())
            block_in.unlink(missing_ok=True)
            block_out.unlink(missing_ok=True)

        write_text(dec_path, b"".join(decrypted_blocks))
        print(
            f" {name.replace('_', '-').upper()} round-trip written to: {enc_path.name} {dec_path.name}"
        )


def hashes_and_signature(
    data: bytes, private_key: Path, public_key: Path, output_dir: Path
) -> None:
    # Dwa hashe, podpis i weryfikacja
    print_section("3) Funkcje skrótu")
    infile = temp_file(data)
    for name, algo in (("sha256", "-sha256"), ("sha512", "-sha512")):
        result = run(
            ["openssl", "dgst", algo, "-hex", str(infile)], capture_output=True
        )
        digest = result.stdout.decode().strip().split()[-1]
        (output_dir / f"{name}.txt").write_text(digest, encoding="utf-8")
        print(f" {name.upper()} digest: {digest[:32]}...")
    infile.unlink(missing_ok=True)

    print_section("4) Podpis cyfrowy")
    infile = temp_file(data)
    signature = output_dir / "signature.bin"
    run(
        [
            "openssl",
            "dgst",
            "-sha256",
            "-sign",
            str(private_key),
            "-out",
            str(signature),
            "-sigopt",
            "rsa_padding_mode:pss",
            "-sigopt",
            "rsa_pss_saltlen:-1",
            str(infile),
        ]
    )
    run(
        [
            "openssl",
            "dgst",
            "-sha256",
            "-verify",
            str(public_key),
            "-signature",
            str(signature),
            "-sigopt",
            "rsa_padding_mode:pss",
            "-sigopt",
            "rsa_pss_saltlen:-1",
            str(infile),
        ]
    )
    infile.unlink(missing_ok=True)
    print(" RSA-PSS signature verification: True")


def run_demo(input_file: Path) -> None:
    # Główna funkcja uruchamiająca
    ensure_openssl_available()
    data = load_input_file(input_file)
    output_dir = input_file.parent / "outputs" / "openssl"
    output_dir.mkdir(parents=True, exist_ok=True)
    print("\n" + "=" * 60)
    print("LIBRARY 1: OpenSSL (CLI)")
    print("=" * 60)
    print(f"Plik wejściowy: {input_file.name}")
    print(f"Rozmiar danych: {len(data)} bytes")
    private_key, public_key = gen_keys(output_dir)
    symmetric(data, output_dir)
    rsa_round_trip(data, private_key, public_key, output_dir)
    hashes_and_signature(data, private_key, public_key, output_dir)
    print("Demo OpenSSL zakończone. Sprawdź katalog outputs/openssl")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Demo OpenSSL CLI na danych z pliku")
    parser.add_argument(
        "input_file",
        nargs="?",
        default="sample_input.txt",
        help="Plik wejściowy do demonstracji",
    )
    return parser.parse_args()


if __name__ == "__main__":
    run_demo(Path(parse_args().input_file))
