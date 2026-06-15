from __future__ import annotations

# Benchmark runner for the hybrid handshake
# It repeatedly calls the client, stores results in CSV form, and optionally
# forwards benchmark telemetry to Application Insights

import argparse
import csv
import os
import time
from typing import Any
import logging
import importlib

try:
    from azure.monitor.opentelemetry import configure_azure_monitor

    HAS_AZURE_MON_SDK = True
except Exception:
    HAS_AZURE_MON_SDK = False


def run_iterations(base_url: str, iterations: int, delay: float, out_file: str) -> int:
    """
    Import the client dynamically so the benchmark can be launched as a script
    """
    sys_path_saved = None
    try:
        import sys

        # Ensure the repository root is available for module resolution
        root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if root not in sys.path:
            sys.path.insert(0, root)

        client_mod = importlib.import_module("client.client")
    except Exception as exc:
        print("failed to import client.client:", exc)
        return 2

    logger = logging.getLogger("benchmark-logger")
    logger.setLevel(logging.INFO)

    # If Azure Monitor SDK is available and we have the connection string, configure it
    if HAS_AZURE_MON_SDK and os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        try:
            configure_azure_monitor()
            logger.info("Azure Monitor configured for benchmark via OpenTelemetry.")
        except Exception as e:
            print(f"Failed to setup Azure Monitor: {e}")

    # Define the CSV field names upfront to prevent IndexError for 0 iterations
    fieldnames = ["iteration", "ok", "elapsed_ms_reported", "wall_ms", "session_id"]
    rows: list[dict[str, Any]] = []

    for i in range(1, iterations + 1):
        # Measure both the result reported by the server and the actual wall clock time taken by the handshake
        t0 = time.time()
        try:
            result = client_mod.run_handshake(base_url.rstrip("/"))
            ok = True
            elapsed = result.elapsed_ms
        except Exception as exc:
            ok = False
            elapsed = -1
            result = None

        wall = int((time.time() - t0) * 1000)
        session_id = getattr(result, "session_id", "")
        row = {
            "iteration": i,
            "ok": ok,
            "elapsed_ms_reported": elapsed,
            "wall_ms": wall,
            "session_id": getattr(result, "session_id", ""),
        }
        rows.append(row)

        # Send one telemetry event per benchmark iteration when Azure Monitor is available
        logger.info(
            f"Benchmark iteration {i} completed.",
            extra={
                "custom_dimensions": {
                    "iteration": str(i),
                    "ok": str(ok),
                    "wall_ms": wall,
                    "elapsed_ms_reported": elapsed,
                    "session_id": session_id,
                }
            },
        )

        print(f"iter={i} ok={ok} wall_ms={wall} elapsed_ms={elapsed}")
        time.sleep(delay)

    # Save the benchmark results for later inspection or reporting
    with open(out_file, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print("wrote", out_file)
    return 0


def main() -> int:
    # Simple CLI so the benchmark can be run locally
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--iterations", type=int, default=5)
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--out", default="benchmarks/results.csv")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    return run_iterations(args.base_url, args.iterations, args.delay, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
