import argparse
import csv
import os
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extensions import connection as PgConnection


ROOT_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT_DIR / "results"
EXPLAIN_DIR = RESULTS_DIR / "explain"


SIZE_CONFIG: Dict[str, Dict[str, int]] = {
    "small": {
        "galaxies": 50,
        "constellations": 88,
        "star_systems": 2_000,
        "stars": 20_000,
        "planets": 100_000,
        "moons": 200_000,
        "telescopes": 200,
        "instruments": 1_000,
        "missions": 2_000,
        "observations": 500_000,
    },
    "medium": {
        "galaxies": 100,
        "constellations": 200,
        "star_systems": 4_000,
        "stars": 40_000,
        "planets": 200_000,
        "moons": 400_000,
        "telescopes": 400,
        "instruments": 2_000,
        "missions": 4_000,
        "observations": 1_000_000,
    },
    "large": {
        "galaxies": 200,
        "constellations": 600,
        "star_systems": 20_000,
        "stars": 200_000,
        "planets": 1_000_000,
        "moons": 2_000_000,
        "telescopes": 1_000,
        "instruments": 5_000,
        "missions": 10_000,
        "observations": 10_000_000,
    },
}


CUSTOM_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_observations_observed_at ON observations(observed_at)",
    "CREATE INDEX IF NOT EXISTS idx_observations_mission_id ON observations(mission_id)",
    "CREATE INDEX IF NOT EXISTS idx_observations_target ON observations(target_type, target_id)",
    "CREATE INDEX IF NOT EXISTS idx_observations_telescope_id ON observations(telescope_id)",
    "CREATE INDEX IF NOT EXISTS idx_observations_instrument_id ON observations(instrument_id)",
    "CREATE INDEX IF NOT EXISTS idx_planets_star_type ON planets(star_id, planet_type)",
    "CREATE INDEX IF NOT EXISTS idx_stars_system_id ON stars(system_id)",
    "CREATE INDEX IF NOT EXISTS idx_star_systems_galaxy_id ON star_systems(galaxy_id)",
    "CREATE INDEX IF NOT EXISTS idx_moons_planet_id ON moons(planet_id)",
    "CREATE INDEX IF NOT EXISTS idx_instruments_telescope_id ON instruments(telescope_id)",
]

DROP_CUSTOM_INDEXES = [
    "DROP INDEX IF EXISTS idx_observations_observed_at",
    "DROP INDEX IF EXISTS idx_observations_mission_id",
    "DROP INDEX IF EXISTS idx_observations_target",
    "DROP INDEX IF EXISTS idx_observations_telescope_id",
    "DROP INDEX IF EXISTS idx_observations_instrument_id",
    "DROP INDEX IF EXISTS idx_planets_star_type",
    "DROP INDEX IF EXISTS idx_stars_system_id",
    "DROP INDEX IF EXISTS idx_star_systems_galaxy_id",
    "DROP INDEX IF EXISTS idx_moons_planet_id",
    "DROP INDEX IF EXISTS idx_instruments_telescope_id",
]


@dataclass
class Scenario:
    key: str
    operation: str
    description: str
    sql: str
    params_fn: Callable[[Dict[str, int]], Dict[str, Any]]


def get_conn() -> PgConnection:
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", "5432")),
        dbname=os.getenv("PGDATABASE", "astronomy"),
        user=os.getenv("PGUSER", "admin"),
        password=os.getenv("PGPASSWORD", "admin"),
    )


def execute_many(cur, sql_statements: List[str]) -> None:
    for stmt in sql_statements:
        cur.execute(stmt)


def truncate_all(cur) -> None:
    cur.execute(
        """
        TRUNCATE TABLE
            observations,
            instruments,
            missions,
            telescopes,
            moons,
            planets,
            stars,
            star_systems,
            constellations,
            galaxies
        RESTART IDENTITY CASCADE
        """
    )


def load_size(size: str) -> None:
    cfg = SIZE_CONFIG[size]
    with get_conn() as conn:
        conn.autocommit = False
        with conn.cursor() as cur:
            print(f"[LOAD] Truncating existing data for size={size}...")
            truncate_all(cur)

            print("[LOAD] Inserting galaxies...")
            cur.execute(
                """
                INSERT INTO galaxies (name, galaxy_type, distance_mly)
                SELECT
                    format('Galaxy-%s', gs),
                    (ARRAY['Spiral', 'Elliptical', 'Irregular', 'Lenticular'])[1 + (gs % 4)],
                    round((gs * 0.37)::numeric, 2)
                FROM generate_series(1, %(count)s) AS gs
                """,
                {"count": cfg["galaxies"]},
            )

            print("[LOAD] Inserting constellations...")
            cur.execute(
                """
                INSERT INTO constellations (name, area_sq_deg)
                SELECT
                    format('Constellation-%s', gs),
                    round((30 + (gs * 3.17 % 900))::numeric, 2)
                FROM generate_series(1, %(count)s) AS gs
                """,
                {"count": cfg["constellations"]},
            )

            print("[LOAD] Inserting star_systems...")
            cur.execute(
                """
                INSERT INTO star_systems (name, galaxy_id, constellation_id, distance_ly)
                SELECT
                    format('System-%s', gs),
                    1 + (gs %% %(galaxies)s),
                    CASE WHEN gs %% 5 = 0 THEN NULL ELSE 1 + (gs %% %(constellations)s) END,
                    round((gs * 0.91)::numeric, 2)
                FROM generate_series(1, %(count)s) AS gs
                """,
                {
                    "count": cfg["star_systems"],
                    "galaxies": cfg["galaxies"],
                    "constellations": cfg["constellations"],
                },
            )

            print("[LOAD] Inserting stars...")
            cur.execute(
                """
                INSERT INTO stars (name, system_id, spectral_type, mass_solar, radius_solar)
                SELECT
                    format('Star-%s', gs),
                    1 + (gs %% %(systems)s),
                    (ARRAY['O5V', 'B2V', 'A0V', 'F5V', 'G2V', 'K0V', 'M3V'])[1 + (gs %% 7)],
                    round((0.08 + (gs %% 300) * 0.01)::numeric, 3),
                    round((0.10 + (gs %% 250) * 0.01)::numeric, 3)
                FROM generate_series(1, %(count)s) AS gs
                """,
                {"count": cfg["stars"], "systems": cfg["star_systems"]},
            )

            print("[LOAD] Inserting planets...")
            cur.execute(
                """
                INSERT INTO planets (name, star_id, planet_type, mass_earth, radius_earth, orbit_period_days)
                SELECT
                    format('Planet-%s', gs),
                    1 + (gs %% %(stars)s),
                    (ARRAY['Terrestrial', 'Gas Giant', 'Ice Giant', 'Super-Earth'])[1 + (gs %% 4)],
                    round((0.1 + (gs %% 1000) * 0.05)::numeric, 3),
                    round((0.2 + (gs %% 500) * 0.02)::numeric, 3),
                    round((10 + (gs %% 3000) * 1.1)::numeric, 2)
                FROM generate_series(1, %(count)s) AS gs
                """,
                {"count": cfg["planets"], "stars": cfg["stars"]},
            )

            print("[LOAD] Inserting moons...")
            cur.execute(
                """
                INSERT INTO moons (name, planet_id, mass_lunar, radius_lunar, orbit_period_days)
                SELECT
                    format('Moon-%s', gs),
                    1 + (gs %% %(planets)s),
                    round((0.001 + (gs %% 2000) * 0.001)::numeric, 3),
                    round((0.01 + (gs %% 700) * 0.005)::numeric, 3),
                    round((0.1 + (gs %% 500) * 0.3)::numeric, 2)
                FROM generate_series(1, %(count)s) AS gs
                """,
                {"count": cfg["moons"], "planets": cfg["planets"]},
            )

            print("[LOAD] Inserting telescopes...")
            cur.execute(
                """
                INSERT INTO telescopes (name, telescope_type, location, aperture_m)
                SELECT
                    format('Telescope-%s', gs),
                    (ARRAY['Space', 'Optical', 'Radio', 'Infrared'])[1 + (gs %% 4)],
                    format('Location-%s', gs %% 100),
                    round((1.5 + (gs %% 200) * 0.15)::numeric, 2)
                FROM generate_series(1, %(count)s) AS gs
                """,
                {"count": cfg["telescopes"]},
            )

            print("[LOAD] Inserting instruments...")
            cur.execute(
                """
                INSERT INTO instruments (name, telescope_id, wavelength_band, resolution_arcsec)
                SELECT
                    format('Instrument-%s', gs),
                    1 + (gs %% %(telescopes)s),
                    (ARRAY['UV-Vis', 'Optical', 'Infrared', 'Radio'])[1 + (gs %% 4)],
                    round((0.005 + (gs %% 1000) * 0.0005)::numeric, 4)
                FROM generate_series(1, %(count)s) AS gs
                """,
                {"count": cfg["instruments"], "telescopes": cfg["telescopes"]},
            )

            print("[LOAD] Inserting missions...")
            cur.execute(
                """
                INSERT INTO missions (name, agency, start_date, end_date)
                SELECT
                    format('Mission-%s', gs),
                    (ARRAY['NASA', 'ESA', 'JAXA', 'CNSA', 'ISRO'])[1 + (gs %% 5)],
                    date '1990-01-01' + ((gs %% 10000) * interval '1 day'),
                    CASE WHEN gs %% 4 = 0 THEN NULL ELSE date '2010-01-01' + ((gs %% 5000) * interval '1 day') END
                FROM generate_series(1, %(count)s) AS gs
                """,
                {"count": cfg["missions"]},
            )

            print("[LOAD] Inserting observations (largest table)...")
            cur.execute(
                """
                INSERT INTO observations (
                    telescope_id,
                    instrument_id,
                    mission_id,
                    target_type,
                    target_id,
                    observed_at,
                    exposure_s
                )
                SELECT
                    1 + (gs %% %(telescopes)s),
                    1 + (gs %% %(instruments)s),
                    CASE WHEN gs %% 10 = 0 THEN NULL ELSE 1 + (gs %% %(missions)s) END,
                    CASE WHEN gs %% 2 = 0 THEN 'star' ELSE 'planet' END,
                    CASE WHEN gs %% 2 = 0 THEN 1 + (gs %% %(stars)s) ELSE 1 + (gs %% %(planets)s) END,
                    now() - ((gs %% 31536000) * interval '1 second'),
                    100 + (gs %% 5000)
                FROM generate_series(1, %(count)s) AS gs
                """,
                {
                    "count": cfg["observations"],
                    "telescopes": cfg["telescopes"],
                    "instruments": cfg["instruments"],
                    "missions": cfg["missions"],
                    "stars": cfg["stars"],
                    "planets": cfg["planets"],
                },
            )

            conn.commit()

    print(f"[LOAD] Completed load for size={size}.")


def create_indexes(conn: PgConnection) -> None:
    with conn.cursor() as cur:
        execute_many(cur, CUSTOM_INDEXES)
    conn.commit()


def drop_indexes(conn: PgConnection) -> None:
    with conn.cursor() as cur:
        execute_many(cur, DROP_CUSTOM_INDEXES)
    conn.commit()


def fetch_max_ids(conn: PgConnection) -> Dict[str, int]:
    tables = [
        "star_systems",
        "stars",
        "planets",
        "missions",
        "observations",
        "telescopes",
        "instruments",
    ]
    max_ids: Dict[str, int] = {}
    with conn.cursor() as cur:
        for tbl in tables:
            cur.execute(f"SELECT COALESCE(MAX(id), 1) FROM {tbl}")
            max_ids[tbl] = int(cur.fetchone()[0])
    return max_ids


def scenarios() -> List[Scenario]:
    return [
        # CREATE (6)
        Scenario(
            "C1",
            "CREATE",
            "Insert single mission",
            """
            INSERT INTO missions(name, agency, start_date, end_date)
            VALUES (%(name)s, 'NASA', CURRENT_DATE, NULL)
            """,
            lambda m: {"name": f"bench-mission-{time.time_ns()}"},
        ),
        Scenario(
            "C2",
            "CREATE",
            "Insert single telescope",
            """
            INSERT INTO telescopes(name, telescope_type, location, aperture_m)
            VALUES (%(name)s, 'Optical', 'Benchmark-Location', 8.20)
            """,
            lambda m: {"name": f"bench-telescope-{time.time_ns()}"},
        ),
        Scenario(
            "C3",
            "CREATE",
            "Insert single star system",
            """
            INSERT INTO star_systems(name, galaxy_id, constellation_id, distance_ly)
            VALUES (%(name)s, 1, 1, 1234.56)
            """,
            lambda m: {"name": f"bench-system-{time.time_ns()}"},
        ),
        Scenario(
            "C4",
            "CREATE",
            "Insert single star",
            """
            INSERT INTO stars(name, system_id, spectral_type, mass_solar, radius_solar)
            VALUES (%(name)s, %(system_id)s, 'G2V', 1.001, 0.998)
            """,
            lambda m: {
                "name": f"bench-star-{time.time_ns()}",
                "system_id": 1 + (time.time_ns() % max(1, m["star_systems"])),
            },
        ),
        Scenario(
            "C5",
            "CREATE",
            "Insert single planet",
            """
            INSERT INTO planets(name, star_id, planet_type, mass_earth, radius_earth, orbit_period_days)
            VALUES (%(name)s, %(star_id)s, 'Terrestrial', 1.02, 1.01, 401.5)
            """,
            lambda m: {
                "name": f"bench-planet-{time.time_ns()}",
                "star_id": 1 + (time.time_ns() % max(1, m["stars"])),
            },
        ),
        Scenario(
            "C6",
            "CREATE",
            "Insert batch of 100 observations",
            """
            INSERT INTO observations(telescope_id, instrument_id, mission_id, target_type, target_id, observed_at, exposure_s)
            SELECT
                1 + (gs %% %(telescopes)s),
                1 + (gs %% %(instruments)s),
                1 + (gs %% %(missions)s),
                CASE WHEN gs %% 2 = 0 THEN 'star' ELSE 'planet' END,
                CASE WHEN gs %% 2 = 0 THEN 1 + (gs %% %(stars)s) ELSE 1 + (gs %% %(planets)s) END,
                now() - ((gs %% 100000) * interval '1 second'),
                100 + (gs %% 5000)
            FROM generate_series(1, 100) gs
            """,
            lambda m: {
                "telescopes": max(1, m["telescopes"]),
                "instruments": max(1, m["instruments"]),
                "missions": max(1, m["missions"]),
                "stars": max(1, m["stars"]),
                "planets": max(1, m["planets"]),
            },
        ),
        # READ (6)
        Scenario(
            "R1",
            "READ",
            "Point lookup observation by PK",
            "SELECT * FROM observations WHERE id = %(id)s",
            lambda m: {"id": 1 + (time.time_ns() % max(1, m["observations"]))},
        ),
        Scenario(
            "R2",
            "READ",
            "Range read by timestamp with limit",
            """
            SELECT id, observed_at, exposure_s
            FROM observations
            WHERE observed_at >= now() - interval '30 days'
            ORDER BY observed_at DESC
            LIMIT 1000
            """,
            lambda m: {},
        ),
        Scenario(
            "R3",
            "READ",
            "Join observations + instruments + telescopes",
            """
            SELECT o.id, o.observed_at, i.name AS instrument_name, t.name AS telescope_name
            FROM observations o
            JOIN instruments i ON i.id = o.instrument_id
            JOIN telescopes t ON t.id = o.telescope_id
            WHERE o.mission_id = %(mission_id)s
            LIMIT 1000
            """,
            lambda m: {"mission_id": 1 + (time.time_ns() % max(1, m["missions"]))},
        ),
        Scenario(
            "R4",
            "READ",
            "Aggregate avg exposure per telescope",
            """
            SELECT o.telescope_id, AVG(o.exposure_s) AS avg_exposure
            FROM observations o
            GROUP BY o.telescope_id
            ORDER BY avg_exposure DESC
            LIMIT 100
            """,
            lambda m: {},
        ),
        Scenario(
            "R5",
            "READ",
            "Filter planets by type and mass",
            """
            SELECT id, name, mass_earth
            FROM planets
            WHERE planet_type = 'Terrestrial' AND mass_earth BETWEEN 0.5 AND 5.0
            ORDER BY mass_earth
            LIMIT 1000
            """,
            lambda m: {},
        ),
        Scenario(
            "R6",
            "READ",
            "Deep join from galaxy to observations",
            """
            SELECT g.id, COUNT(o.id) AS obs_count
            FROM galaxies g
            JOIN star_systems ss ON ss.galaxy_id = g.id
            JOIN stars s ON s.system_id = ss.id
            JOIN planets p ON p.star_id = s.id
            LEFT JOIN observations o
              ON (o.target_type = 'planet' AND o.target_id = p.id)
              OR (o.target_type = 'star' AND o.target_id = s.id)
            WHERE g.id = %(galaxy_id)s
            GROUP BY g.id
            """,
            lambda m: {"galaxy_id": 1},
        ),
        # UPDATE (6)
        Scenario(
            "U1",
            "UPDATE",
            "Update one observation by PK",
            "UPDATE observations SET exposure_s = exposure_s + 1 WHERE id = %(id)s",
            lambda m: {"id": 1 + (time.time_ns() % max(1, m["observations"]))},
        ),
        Scenario(
            "U2",
            "UPDATE",
            "Batch update 500 observations by mission",
            """
            WITH cte AS (
                SELECT id
                FROM observations
                WHERE mission_id = %(mission_id)s
                LIMIT 500
            )
            UPDATE observations o
            SET exposure_s = o.exposure_s + 2
            FROM cte
            WHERE o.id = cte.id
            """,
            lambda m: {"mission_id": 1 + (time.time_ns() % max(1, m["missions"]))},
        ),
        Scenario(
            "U3",
            "UPDATE",
            "Batch update 200 planets",
            """
            WITH cte AS (
                SELECT id
                FROM planets
                WHERE star_id BETWEEN 1 AND LEAST(%(stars)s, 10000)
                LIMIT 200
            )
            UPDATE planets p
            SET orbit_period_days = orbit_period_days * 1.0001
            FROM cte
            WHERE p.id = cte.id
            """,
            lambda m: {"stars": max(1, m["stars"])},
        ),
        Scenario(
            "U4",
            "UPDATE",
            "Batch update 200 stars",
            """
            WITH cte AS (
                SELECT id
                FROM stars
                WHERE id <= LEAST(%(stars)s, 20000)
                LIMIT 200
            )
            UPDATE stars s
            SET radius_solar = radius_solar * 1.0001
            FROM cte
            WHERE s.id = cte.id
            """,
            lambda m: {"stars": max(1, m["stars"])},
        ),
        Scenario(
            "U5",
            "UPDATE",
            "Batch update 100 missions",
            """
            WITH cte AS (
                SELECT id
                FROM missions
                WHERE end_date IS NULL
                LIMIT 100
            )
            UPDATE missions m
            SET end_date = CURRENT_DATE
            FROM cte
            WHERE m.id = cte.id
            """,
            lambda m: {},
        ),
        Scenario(
            "U6",
            "UPDATE",
            "Batch update 100 instruments",
            """
            WITH cte AS (
                SELECT id
                FROM instruments
                LIMIT 100
            )
            UPDATE instruments i
            SET resolution_arcsec = resolution_arcsec * 0.999
            FROM cte
            WHERE i.id = cte.id
            """,
            lambda m: {},
        ),
        # DELETE (6)
        Scenario(
            "D1",
            "DELETE",
            "Delete one observation by PK",
            "DELETE FROM observations WHERE id = %(id)s",
            lambda m: {"id": 1 + (time.time_ns() % max(1, m["observations"]))},
        ),
        Scenario(
            "D2",
            "DELETE",
            "Delete 100 observations by id range",
            """
            WITH cte AS (
                SELECT id
                FROM observations
                WHERE id BETWEEN %(start_id)s AND %(end_id)s
                LIMIT 100
            )
            DELETE FROM observations o
            USING cte
            WHERE o.id = cte.id
            """,
            lambda m: {
                "start_id": 1 + (time.time_ns() % max(1, m["observations"] - 1000)),
                "end_id": min(m["observations"], 10_000_000),
            },
        ),
        Scenario(
            "D3",
            "DELETE",
            "Delete 500 observations for one mission",
            """
            WITH cte AS (
                SELECT id
                FROM observations
                WHERE mission_id = %(mission_id)s
                LIMIT 500
            )
            DELETE FROM observations o
            USING cte
            WHERE o.id = cte.id
            """,
            lambda m: {"mission_id": 1 + (time.time_ns() % max(1, m["missions"]))},
        ),
        Scenario(
            "D4",
            "DELETE",
            "Delete 500 star-target observations",
            """
            WITH cte AS (
                SELECT id
                FROM observations
                WHERE target_type = 'star'
                LIMIT 500
            )
            DELETE FROM observations o
            USING cte
            WHERE o.id = cte.id
            """,
            lambda m: {},
        ),
        Scenario(
            "D5",
            "DELETE",
            "Delete 500 old observations",
            """
            WITH cte AS (
                SELECT id
                FROM observations
                WHERE observed_at < now() - interval '180 days'
                LIMIT 500
            )
            DELETE FROM observations o
            USING cte
            WHERE o.id = cte.id
            """,
            lambda m: {},
        ),
        Scenario(
            "D6",
            "DELETE",
            "Delete 500 low-exposure observations",
            """
            WITH cte AS (
                SELECT id
                FROM observations
                WHERE exposure_s < 500
                LIMIT 500
            )
            DELETE FROM observations o
            USING cte
            WHERE o.id = cte.id
            """,
            lambda m: {},
        ),
    ]


def run_scenario_trial(
    conn: PgConnection, scenario: Scenario, params: Dict[str, Any]
) -> float:
    with conn.cursor() as cur:
        cur.execute("BEGIN")
        try:
            start = time.perf_counter()
            cur.execute(scenario.sql, params)
            # Materialize READ workloads so the benchmark includes transfer/fetch cost.
            if scenario.operation == "READ":
                cur.fetchall()
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            cur.execute("ROLLBACK")
            return elapsed_ms
        except Exception:
            cur.execute("ROLLBACK")
            raise


def run_explain(
    conn: PgConnection,
    selected: List[Scenario],
    max_ids: Dict[str, int],
    size: str,
    mode: str,
) -> None:
    EXPLAIN_DIR.mkdir(parents=True, exist_ok=True)
    out_path = (
        EXPLAIN_DIR
        / f"postgres_explain_{size}_{mode}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )

    with conn.cursor() as cur, out_path.open("w", encoding="utf-8") as f:
        for sc in selected:
            params = sc.params_fn(max_ids)
            cur.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) {sc.sql}", params)
            plan_rows = cur.fetchall()
            f.write(f"\n=== {sc.key} | {sc.description} ===\n")
            for row in plan_rows:
                f.write(row[0] + "\n")

    print(f"[BENCH] Saved EXPLAIN plans: {out_path}")


def run_bench(size: str, trials: int = 3) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    rows: List[Dict[str, Any]] = []

    with get_conn() as conn:
        conn.autocommit = False

        max_ids = fetch_max_ids(conn)
        all_scenarios = scenarios()

        for mode in ["before_indexes", "after_indexes"]:
            if mode == "before_indexes":
                drop_indexes(conn)
            else:
                create_indexes(conn)

            # Refresh planner stats for fairer comparison after structural changes.
            with conn.cursor() as cur:
                cur.execute("ANALYZE")
            conn.commit()

            print(f"[BENCH] Running mode={mode}...")
            for sc in all_scenarios:
                trial_values: List[float] = []
                for trial in range(1, trials + 1):
                    params = sc.params_fn(max_ids)
                    elapsed_ms = run_scenario_trial(conn, sc, params)
                    trial_values.append(elapsed_ms)
                    rows.append(
                        {
                            "database": "postgres",
                            "size": size,
                            "index_mode": mode,
                            "scenario": sc.key,
                            "operation": sc.operation,
                            "description": sc.description,
                            "trial": trial,
                            "elapsed_ms": round(elapsed_ms, 3),
                        }
                    )

                avg_ms = sum(trial_values) / len(trial_values)
                print(
                    f"[BENCH] {mode} | {sc.key} {sc.operation:<6} | "
                    f"avg={avg_ms:10.3f} ms | trials={', '.join(f'{x:.3f}' for x in trial_values)}"
                )

            # Save EXPLAIN for READ scenarios in each mode.
            read_scenarios = [s for s in all_scenarios if s.operation == "READ"]
            run_explain(conn, read_scenarios, max_ids, size, mode)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = RESULTS_DIR / f"postgres_benchmark_{size}_{ts}.csv"
    fieldnames = [
        "database",
        "size",
        "index_mode",
        "scenario",
        "operation",
        "description",
        "trial",
        "elapsed_ms",
    ]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"[BENCH] Saved benchmark CSV: {out_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="PostgreSQL benchmark runner")
    sub = parser.add_subparsers(dest="command", required=True)

    load_cmd = sub.add_parser("load", help="Generate data for selected size")
    load_cmd.add_argument("--size", choices=SIZE_CONFIG.keys(), required=True)

    bench_cmd = sub.add_parser("bench", help="Run benchmark scenarios")
    bench_cmd.add_argument("--size", choices=SIZE_CONFIG.keys(), required=True)
    bench_cmd.add_argument("--trials", type=int, default=3)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "load":
        load_size(args.size)
    elif args.command == "bench":
        run_bench(args.size, args.trials)


if __name__ == "__main__":
    main()
