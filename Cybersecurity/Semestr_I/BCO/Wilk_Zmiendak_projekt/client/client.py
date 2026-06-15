from __future__ import annotations

# Client for the hybrid-channel
# This file connects to the Azure-hosted FastAPI server, verifies the handshake,
# and checks that both sides derive the same session key

import argparse
import base64
import hashlib
import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from pqcrypto.kem import ml_kem_768
from pqcrypto.sign import ml_dsa_65

# -------------------------------------------
# Small utility helpers for encoding and hashing values used in the protocol
# -------------------------------------------


def b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def b64decode(data: str) -> bytes:
    return base64.b64decode(data.encode("ascii"), validate=True)


def canonical_json(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def derive_session_key(
    ecc_secret: bytes,
    kem_secret: bytes,
    session_id: str,
    client_nonce: bytes,
    server_nonce: bytes,
) -> bytes:
    """Combine the classical ECDH secret and the post-quantum ML-KEM secret,
    then stretch the result with HKDF to get one shared 32-byte session key"""
    combined_secret = hashlib.sha256(ecc_secret + kem_secret).digest()
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=hashlib.sha256(server_nonce + client_nonce).digest(),
        info=f"hybrid-channel-v1|{session_id}".encode("utf-8"),
    )
    return hkdf.derive(combined_secret)


def http_get(base_url: str, path: str) -> dict[str, Any]:
    """Issue a GET request and parse the JSON response from the server"""
    with urllib.request.urlopen(f"{base_url}{path}") as response:
        return json.loads(response.read().decode("utf-8"))


def http_post(base_url: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Issue a POST request with a JSON body and parse the JSON response"""
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def load_ec_public_key(raw_public_key: bytes) -> ec.EllipticCurvePublicKey:
    return ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), raw_public_key)


def verify_ecdsa_signature(public_key: bytes, message: bytes, signature: bytes) -> None:
    """Validate the server's classical ECDSA signature over the transcript"""
    key = load_ec_public_key(public_key)
    key.verify(signature, message, ec.ECDSA(hashes.SHA256()))


def verify_ml_dsa_signature(
    public_key: bytes, message: bytes, signature: bytes
) -> None:
    """Validate the server's post-quantum ML-DSA signature over the transcript"""
    try:
        valid = ml_dsa_65.verify(public_key, message, signature)
    except TypeError:
        valid = ml_dsa_65.verify(signature, message, public_key)
    if not valid:
        raise ValueError("ML-DSA signature verification failed")


@dataclass
class HandshakeResult:
    """Compact result object used by the CLI output and benchmarks"""

    session_id: str
    session_key_fingerprint: str
    transcript_hash: str
    elapsed_ms: int


def run_handshake(base_url: str) -> HandshakeResult:
    # Confirm the server is reachable
    health = http_get(base_url, "/health")
    if health.get("status") != "ok":
        raise RuntimeError("server is not healthy")

    # Generate a deterministic client nonce for repeatable testing
    client_nonce = hashlib.sha256(b"hybrid-client-nonce").digest()[:16]
    hello = http_post(
        base_url,
        "/api/v1/hello",
        {"client_nonce": b64encode(client_nonce)},
    )

    # Decode the server's response fields and verify its signatures
    server_nonce = b64decode(hello["server_nonce"])
    server_ecc_public_key = b64decode(hello["server_ecc_public_key"])
    server_ml_kem_public_key = b64decode(hello["server_ml_kem_public_key"])

    # Takes valid keys from the response with the lt_ prefix consistent with app.py
    server_ml_dsa_public_key = b64decode(hello["lt_ml_dsa_public_key"])
    ecdsa_signature = b64decode(hello["lt_ecdsa_signature"])
    ml_dsa_signature = b64decode(hello["lt_ml_dsa_signature"])

    # Recreate the identical transcript dictionary (must be 1:1 with the server)
    hello_transcript = canonical_json(
        {
            "session_id": hello["session_id"],
            "server_nonce": hello["server_nonce"],
            "server_ecc_public_key": hello["server_ecc_public_key"],
            "server_ml_kem_public_key": hello["server_ml_kem_public_key"],
            "lt_ecdsa_public_key": hello["lt_ecdsa_public_key"],
            "lt_ml_dsa_public_key": hello["lt_ml_dsa_public_key"],
            "client_nonce": b64encode(client_nonce),
            "algorithms": hello["algorithms"],
        }
    )

    # To verify the ECDSA signature, we pass the long-term server key (hello["lt_ecdsa_public_key"])
    verify_ecdsa_signature(
        b64decode(hello["lt_ecdsa_public_key"]), hello_transcript, ecdsa_signature
    )
    verify_ml_dsa_signature(
        server_ml_dsa_public_key, hello_transcript, ml_dsa_signature
    )

    # Create the client's ECC key pair and perform the ML-KEM exchange
    client_private_key = ec.generate_private_key(ec.SECP256R1())
    client_public_key = client_private_key.public_key().public_bytes(
        encoding=Encoding.X962,
        format=PublicFormat.UncompressedPoint,
    )

    client_ml_kem_ciphertext, client_ml_kem_shared_secret = ml_kem_768.encrypt(
        server_ml_kem_public_key
    )

    finish = http_post(
        base_url,
        "/api/v1/finish",
        {
            "session_id": hello["session_id"],
            "client_nonce": b64encode(client_nonce),
            "client_ecc_public_key": b64encode(client_public_key),
            "client_ml_kem_ciphertext": b64encode(client_ml_kem_ciphertext),
        },
    )

    if finish.get("status") not in {"established", "ok"}:
        raise RuntimeError("handshake was not established")

    # Derive the same session key locally and compare fingerprints
    derived_client_key = derive_session_key(
        ecc_secret=client_private_key.exchange(
            ec.ECDH(),
            load_ec_public_key(server_ecc_public_key),
        ),
        kem_secret=client_ml_kem_shared_secret,
        session_id=hello["session_id"],
        client_nonce=client_nonce,
        server_nonce=server_nonce,
    )

    print("server health:", health)
    print("session id:", hello["session_id"])
    print("algorithms:", ", ".join(hello["algorithms"]))
    print("server nonce:", b64encode(server_nonce))
    print("session key fingerprint:", finish["session_key_fingerprint"])
    print("local derived key fingerprint:", sha256_hex(derived_client_key))

    if sha256_hex(derived_client_key) != finish["session_key_fingerprint"]:
        raise RuntimeError("session key fingerprints do not match")

    return HandshakeResult(
        session_id=hello["session_id"],
        session_key_fingerprint=finish["session_key_fingerprint"],
        transcript_hash=finish["transcript_hash"],
        elapsed_ms=int(finish["elapsed_ms"]),
    )


def main() -> int:
    """CLI entry point used for local testing and Azure verification"""
    parser = argparse.ArgumentParser(description="Client for the hybrid Azure server.")
    parser.add_argument(
        "--base-url", default="http://127.0.0.1:8000", help="Server base URL"
    )
    args = parser.parse_args()

    try:
        result = run_handshake(args.base_url.rstrip("/"))
    except (urllib.error.URLError, InvalidSignature, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result.__dict__, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
