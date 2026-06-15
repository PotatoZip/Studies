from __future__ import annotations

import base64
import hashlib
import json
import logging
import os
import secrets
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pqcrypto.kem import ml_kem_768
from pqcrypto.sign import ml_dsa_65

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging

_KEYS_DIR = Path(os.getenv("LT_KEYS_DIR", "."))
_LT_ECDSA_PRIVATE_PEM = _KEYS_DIR / "lt_ecdsa_private.pem"
_LT_ML_DSA_SECRET_BIN = _KEYS_DIR / "lt_ml_dsa_secret.bin"
_LT_ML_DSA_PUBLIC_BIN = _KEYS_DIR / "lt_ml_dsa_public.bin"


def b64encode(data: bytes) -> str:
    """Encode raw bytes to a URL-safe ASCII base64 string"""
    return base64.b64encode(data).decode("ascii")


def b64decode(data: str) -> bytes:
    """Decode a base64 string back to raw bytes"""
    try:
        return base64.b64decode(data.encode("ascii"), validate=True)
    except Exception as exc:
        raise ValueError("invalid base64 data") from exc


def canonical_json(payload: dict[str, Any]) -> bytes:
    """Produce a deterministic, compact JSON byte string from a dict"""
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    """Return the lowercase hex SHA-256 digest of data"""
    return hashlib.sha256(data).hexdigest()


def generate_ec_keypair() -> tuple[ec.EllipticCurvePrivateKey, bytes]:
    """
    Generate a fresh ephemeral P-256 (SECP256R1) key pair for ONE session
    Returns the private key object and the uncompressed public key bytes (04 || X || Y format, 65 bytes)
    This key pair is used for ECDH only authentication is done by the long-term keys, not these ephemeral ones
    """
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_bytes = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint,
    )
    return private_key, public_bytes


def ecdsa_sign(private_key: ec.EllipticCurvePrivateKey, message: bytes) -> bytes:
    """
    Sign message with the given P-256 private key using ECDSA-SHA256
    In this protocol, only the LONG-TERM ECDSA key calls this function
    """
    return private_key.sign(message, ec.ECDSA(hashes.SHA256()))


def _load_or_create_lt_ecdsa_key() -> ec.EllipticCurvePrivateKey:
    """
    Load the server's long-term ECDSA private key from disk, or generate and persist a new one if the key file does not yet exist
    The key is stored as an unencrypted PEM file
    """
    if _LT_ECDSA_PRIVATE_PEM.exists():
        pem_data = _LT_ECDSA_PRIVATE_PEM.read_bytes()
        key = serialization.load_pem_private_key(pem_data, password=None)
        return key

    # On first run it generates and persists a new long-term key pair
    key = ec.generate_private_key(ec.SECP256R1())
    _LT_ECDSA_PRIVATE_PEM.write_bytes(
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    return key


def _load_or_create_lt_ml_dsa_keys() -> tuple[bytes, bytes]:
    """
    Load the server's long-term ML-DSA-65 key pair from disk, or generate and persist a new pair if the files do not yet exist
    Returns (public_key_bytes, secret_key_bytes).
    """
    if _LT_ML_DSA_SECRET_BIN.exists() and _LT_ML_DSA_PUBLIC_BIN.exists():
        return (
            _LT_ML_DSA_PUBLIC_BIN.read_bytes(),
            _LT_ML_DSA_SECRET_BIN.read_bytes(),
        )

    # On first run it generates and persists a new long-term ML-DSA key pair
    public_key, secret_key = ml_dsa_65.generate_keypair()
    _LT_ML_DSA_PUBLIC_BIN.write_bytes(public_key)
    _LT_ML_DSA_SECRET_BIN.write_bytes(secret_key)
    return public_key, secret_key


def pq_generate_kem_keypair() -> tuple[bytes, bytes]:
    """
    Generate a fresh ephemeral ML-KEM-768 key pair for ONE session
    Returns (public_key, secret_key) as raw byte strings
    ML-KEM-768 public keys are 1 184 bytes, secret keys are 2 400 bytes
    These keys are discarded after the session's finish step completes
    """
    public_key, secret_key = ml_kem_768.generate_keypair()
    return public_key, secret_key


def pq_kem_decrypt(secret_key: bytes, ciphertext: bytes) -> bytes:
    """Decapsulate a ML-KEM-768 ciphertext to recover the 32-byte shared secret"""
    try:
        return ml_kem_768.decrypt(secret_key, ciphertext)
    except TypeError:
        return ml_kem_768.decrypt(ciphertext, secret_key)


def pq_sign(secret_key: bytes, message: bytes) -> bytes:
    """
    Sign message with a ML-DSA-65 secret key and return the signature bytes
    ML-DSA-65 signatures are 3 309 bytes, compare this with the ~72-byte
    ECDSA-SHA256 signature to see the bandwidth cost of post-quantum auth
    """
    try:
        return ml_dsa_65.sign(secret_key, message)
    except TypeError:
        return ml_dsa_65.sign(message, secret_key)


def pq_verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    """
    Verify a ML-DSA-65 signature, returns True on success, False otherwise
    Used internally during the finish step to double-check the server's own long-term signature if needed for logging/audit purposes
    """
    try:
        result = ml_dsa_65.verify(public_key, message, signature)
    except TypeError:
        result = ml_dsa_65.verify(signature, message, public_key)
    return bool(result)


def derive_session_key(
    ecc_secret: bytes,
    kem_secret: bytes,
    session_id: str,
    client_nonce: bytes,
    server_nonce: bytes,
) -> bytes:
    """Derive a 32-byte symmetric session key from both classical and PQ secrets"""
    combined_secret = hashlib.sha256(ecc_secret + kem_secret).digest()
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=hashlib.sha256(server_nonce + client_nonce).digest(),
        info=f"hybrid-channel-v1|{session_id}".encode("utf-8"),
    )
    return hkdf.derive(combined_secret)


class HelloRequest(BaseModel):
    """
    Client -> Server: first handshake message
    The client sends its nonce so that both sides include it in the signed transcript, binding the server's signature to this specific client
    """

    client_nonce: str | None = Field(
        default=None, description="Client nonce (16 bytes, base64-encoded)"
    )


class HelloResponse(BaseModel):
    """
    Server -> Client: first handshake reply
    Contains the server's ephemeral public keys for this session and the long-term public keys that the client uses for identity verification
    Both a classical (ECDSA) and a post-quantum (ML-DSA) signature are included so that the client can verify with whichever algorithm it trusts
    """

    session_id: str
    server_nonce: str
    server_ecc_public_key: str  # 65 bytes (uncompressed P-256 point)
    server_ml_kem_public_key: str  # 1 184 bytes (ML-KEM-768)
    lt_ecdsa_public_key: str  # 65 bytes (long-term P-256 point)
    lt_ml_dsa_public_key: str  # 1 952 bytes (ML-DSA-65)
    lt_ecdsa_signature: str  # ~72 bytes (DER ECDSA-SHA256)
    lt_ml_dsa_signature: str  # 3 309 bytes (ML-DSA-65)
    transcript_hash: str  # SHA-256 hex of the signed transcript
    algorithms: list[str]


class PubkeysResponse(BaseModel):
    """
    Server -> Client: long-term public key export
    Returned by GET /api/v1/pubkeys
    """

    lt_ecdsa_public_key: str
    lt_ml_dsa_public_key: str
    note: str


class FinishRequest(BaseModel):
    """
    Client -> Server: second handshake message
    Carries the client's ephemeral ECC public key and the ML-KEM ciphertext
    """

    session_id: str
    client_nonce: str
    client_ecc_public_key: str
    client_ml_kem_ciphertext: str


class FinishResponse(BaseModel):
    """
    Server -> Client: handshake confirmation
    Returns the SHA-256 fingerprint of the derived session key so the client can confirm that both sides computed the same value
    """

    session_id: str
    status: str
    session_key_fingerprint: str
    transcript_hash: str
    elapsed_ms: int


@dataclass
class HandshakeState:
    """
    All ephemeral material the server must remember between hello and finish
    Stored in the in-process SERVER_STATE dict, keyed by session_id
    """

    session_id: str
    created_at: float
    server_nonce: bytes
    server_ecc_private_key: ec.EllipticCurvePrivateKey
    server_ecc_public_key: bytes
    server_ml_kem_public_key: bytes
    server_ml_kem_secret_key: bytes
    hello_transcript: bytes


app = FastAPI(
    title="Hybrid Channel Demo Server",
    version="0.2.0",
    description=(
        "Azure-hosted test server for the hybrid ECC + ML-KEM + ML-DSA handshake "
        "Implements a Composite KEM (Dual-KEM) pattern per BSI TR-02102-1 and "
        "ANSSI post-quantum migration guidance"
    ),
)

# Active handshake sessions (session_id -> HandshakeState)
SERVER_STATE: dict[str, HandshakeState] = {}

# How long a session can remain in SERVER_STATE without being completed before it is considered stale and eligible for cleanup
SESSION_TTL_SECONDS: int = 120


@app.on_event("startup")
def load_keys() -> None:
    """
    Run once when the ASGI server starts
    Responsibilities:
      1. Record the bootstrap timestamp (used by /health)
      2. Configure structured logging to stdout
      3. Load or generate the server's long-term identity key pairs and store them in app.state
      4. Initialise the optional Application Insights telemetry client
    """
    app.state.bootstrap_time = time.time()

    # Structured logging (Azure App Service captures stdout automatically)
    logging.basicConfig(level=logging.INFO)
    app.state.logger = logging.getLogger("hybrid-channel")

    try:
        configure_azure_monitor()
        FastAPIInstrumentor.instrument_app(app)
        app.state.logger.info(
            "Application Insights telemetry configured via OpenTelemetry"
        )
    except Exception as e:
        app.state.logger.error(f"Failed to configure Azure Monitor: {e}")

    # Long-term identity keys
    # These are the keys whose public halves user pin in server_keys.json
    app.state.lt_ecdsa_private_key = _load_or_create_lt_ecdsa_key()
    app.state.lt_ecdsa_public_key_bytes = (
        app.state.lt_ecdsa_private_key.public_key().public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )
    )
    app.state.lt_ml_dsa_public_key, app.state.lt_ml_dsa_secret_key = (
        _load_or_create_lt_ml_dsa_keys()
    )

    app.state.logger.info(
        "long-term keys loaded",
        extra={
            "lt_ecdsa_public_key": b64encode(app.state.lt_ecdsa_public_key_bytes)[:20]
            + "…",
            "lt_ml_dsa_public_key": b64encode(app.state.lt_ml_dsa_public_key)[:20]
            + "…",
        },
    )


def _evict_stale_sessions() -> None:
    """
    Remove sessions that were started but never completed within SESSION_TTL_SECONDS
    Called at the start of each hello()
    """
    now = time.time()
    stale = [
        sid
        for sid, state in SERVER_STATE.items()
        if now - state.created_at > SESSION_TTL_SECONDS
    ]
    for sid in stale:
        del SERVER_STATE[sid]
    if stale:
        app.state.logger.info("evicted stale sessions", extra={"count": len(stale)})


@app.get("/health")
def health() -> dict[str, Any]:
    """
    Liveness probe used by Azure App Service and the client's pre-flight check
    Returns uptime and the count of currently active sessions
    """
    uptime = int(time.time() - app.state.bootstrap_time)
    app.state.logger.info("health check", extra={"uptime_seconds": uptime})
    return {
        "status": "ok",
        "service": "hybrid-channel-demo-server",
        "uptime_seconds": uptime,
        "active_sessions": len(SERVER_STATE),
    }


@app.get("/")
def root() -> dict[str, Any]:
    """Service discovery endpoint listing all available API routes"""
    return {
        "name": "Hybrid Channel Demo Server",
        "purpose": "Azure test backend for ECC + ML-KEM + ML-DSA hybrid handshake",
        "endpoints": [
            "/health",
            "/api/v1/pubkeys",
            "/api/v1/hello",
            "/api/v1/finish",
        ],
    }


@app.get("/api/v1/pubkeys", response_model=PubkeysResponse)
def pubkeys() -> PubkeysResponse:
    """
    Return the server's long-term public keys for client-side pinning
    User call this once and save the result to server_keys.json
    All subsequent client runs load that file and use the pinned keys to authenticate the server's hello message
    """
    return PubkeysResponse(
        lt_ecdsa_public_key=b64encode(app.state.lt_ecdsa_public_key_bytes),
        lt_ml_dsa_public_key=b64encode(app.state.lt_ml_dsa_public_key),
        note=(
            "Save this file as server_keys.json and pass it to the client with "
            "--keys-file server_keys.json before running the handshake."
        ),
    )


@app.post("/api/v1/hello", response_model=HelloResponse)
def hello(request: HelloRequest) -> HelloResponse:
    """
    Phase one of the hybrid handshake (server key advertisement and transcript signing)

    Steps performed:
      1. Generate a fresh session_id and server nonce
      2. Generate a fresh ephemeral P-256 key pair for ECDH
      3. Generate a fresh ephemeral ML-KEM-768 key pair for PQ key exchange
      4. Build the hello transcrip
      5. Sign the transcript twice with the LONG-TERM ECDSA and ML-DSA keys
      6. Store the ephemeral state so that the finish endpoint can complete the key derivation
    """
    _evict_stale_sessions()

    session_id = str(uuid.uuid4())
    server_nonce = secrets.token_bytes(16)

    server_ecc_private_key, server_ecc_public_key = generate_ec_keypair()
    server_ml_kem_public_key, server_ml_kem_secret_key = pq_generate_kem_keypair()

    payload = {
        "session_id": session_id,
        "server_nonce": b64encode(server_nonce),
        "server_ecc_public_key": b64encode(server_ecc_public_key),
        "server_ml_kem_public_key": b64encode(server_ml_kem_public_key),
        "lt_ecdsa_public_key": b64encode(app.state.lt_ecdsa_public_key_bytes),
        "lt_ml_dsa_public_key": b64encode(app.state.lt_ml_dsa_public_key),
        "client_nonce": request.client_nonce,
        "algorithms": ["ECC-P256", "ML-KEM-768", "ML-DSA-65"],
    }
    hello_transcript = canonical_json(payload)

    lt_ecdsa_signature = ecdsa_sign(app.state.lt_ecdsa_private_key, hello_transcript)
    lt_ml_dsa_signature = pq_sign(app.state.lt_ml_dsa_secret_key, hello_transcript)

    SERVER_STATE[session_id] = HandshakeState(
        session_id=session_id,
        created_at=time.time(),
        server_nonce=server_nonce,
        server_ecc_private_key=server_ecc_private_key,
        server_ecc_public_key=server_ecc_public_key,
        server_ml_kem_public_key=server_ml_kem_public_key,
        server_ml_kem_secret_key=server_ml_kem_secret_key,
        hello_transcript=hello_transcript,
    )

    # Emit a telemetry event so the Azure dashboard shows handshake activity
    try:
        if getattr(app.state, "telemetry", None):
            app.state.telemetry.track_event(
                "hello",
                {
                    "session_id": session_id,
                    "algorithms": ",".join(payload["algorithms"]),
                },
            )
            app.state.telemetry.flush()
    except Exception:
        app.state.logger.exception("failed to send hello telemetry")

    app.state.logger.info("hello created", extra={"session_id": session_id})

    return HelloResponse(
        session_id=session_id,
        server_nonce=b64encode(server_nonce),
        server_ecc_public_key=b64encode(server_ecc_public_key),
        server_ml_kem_public_key=b64encode(server_ml_kem_public_key),
        lt_ecdsa_public_key=b64encode(app.state.lt_ecdsa_public_key_bytes),
        lt_ml_dsa_public_key=b64encode(app.state.lt_ml_dsa_public_key),
        lt_ecdsa_signature=b64encode(lt_ecdsa_signature),
        lt_ml_dsa_signature=b64encode(lt_ml_dsa_signature),
        transcript_hash=sha256_hex(hello_transcript),
        algorithms=["ECC-P256", "ML-KEM-768", "ML-DSA-65"],
    )


@app.post("/api/v1/finish", response_model=FinishResponse)
def finish(request: FinishRequest) -> FinishResponse:
    """
    Phase two of the hybrid handshake (key derivation and session establishment)

    Steps performed:
      1. Look up the ephemeral session state saved during hello()
      2. Decode and validate the client's ECC public key
      3. Perform ECDH: server ephemeral private x client ephemeral public
      4. Perform ML-KEM decapsulation
      5. Feed both secrets into derive_session_key() which runs HKDF to produce a single 32-byte session key
      6. Return the SHA-256 fingerprint of the session key so the client can confirm both sides derived identical material
      7. Clean up the session from SERVER_STATE
    """
    started_at = time.time()
    state = SERVER_STATE.get(request.session_id)
    if state is None:
        raise HTTPException(status_code=404, detail="unknown session_id")

    try:
        client_nonce = b64decode(request.client_nonce)
        client_ecc_public_key_bytes = b64decode(request.client_ecc_public_key)
        client_ml_kem_ciphertext = b64decode(request.client_ml_kem_ciphertext)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        client_ecc_public_key = ec.EllipticCurvePublicKey.from_encoded_point(
            ec.SECP256R1(), client_ecc_public_key_bytes
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail="invalid client ECC public key"
        ) from exc

    ecc_secret = state.server_ecc_private_key.exchange(ec.ECDH(), client_ecc_public_key)

    kem_secret = pq_kem_decrypt(
        state.server_ml_kem_secret_key, client_ml_kem_ciphertext
    )

    session_key = derive_session_key(
        ecc_secret,
        kem_secret,
        state.session_id,
        client_nonce,
        state.server_nonce,
    )

    elapsed = int((time.time() - started_at) * 1000)

    del SERVER_STATE[request.session_id]

    # Emit a telemetry event for the completed handshake
    try:
        if getattr(app.state, "telemetry", None):
            app.state.telemetry.track_event(
                "finish",
                {"session_id": state.session_id, "status": "established"},
                {"elapsed_ms": elapsed},
            )
            app.state.telemetry.flush()
    except Exception:
        app.state.logger.exception("failed to send finish telemetry")

    app.state.logger.info(
        "handshake finished",
        extra={"session_id": state.session_id, "elapsed_ms": elapsed},
    )

    return FinishResponse(
        session_id=state.session_id,
        status="established",
        session_key_fingerprint=sha256_hex(session_key),
        transcript_hash=sha256_hex(state.hello_transcript),
        elapsed_ms=elapsed,
    )
