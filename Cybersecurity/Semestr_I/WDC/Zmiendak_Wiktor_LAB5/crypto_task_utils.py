from __future__ import annotations

import struct
from pathlib import Path


def load_input_file(path: Path) -> bytes:
    if not path.exists():
        raise FileNotFoundError(f"Brak pliku wejściowego: {path}")
    return path.read_bytes()


def write_text(path: Path, text: bytes) -> None:
    path.write_text(text.decode("utf-8", errors="replace"), encoding="utf-8")


def print_section(title: str) -> None:
    print("\n" + "-" * 60)
    print(title)
    print("-" * 60)


def chunk_data(data: bytes, chunk_size: int) -> list[bytes]:
    return [
        data[index : index + chunk_size] for index in range(0, len(data), chunk_size)
    ]


def pack_blocks(blocks: list[bytes]) -> bytes:
    payload = bytearray()
    for block in blocks:
        payload.extend(struct.pack(">I", len(block)))
        payload.extend(block)
    return bytes(payload)


def unpack_blocks(payload: bytes) -> list[bytes]:
    blocks: list[bytes] = []
    offset = 0
    while offset < len(payload):
        (length,) = struct.unpack_from(">I", payload, offset)
        offset += 4
        blocks.append(payload[offset : offset + length])
        offset += length
    return blocks
