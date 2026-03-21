import argparse
import time
from datetime import datetime, timedelta

import pymysql

from benchmark_shared import bench_mysql


SIZE_CONFIG = {
    "small": {"observations": 500_000},
    "medium": {"observations": 1_000_000},
    "large": {"observations": 10_000_000},
}


def mysql_conn():
    return pymysql.connect(
        host="localhost",
        port=3307,
        user="admin",
        password="admin",
        database="astronomy",
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def reset_seed(cur):
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("TRUNCATE TABLE observations")
    cur.execute("TRUNCATE TABLE instruments")
    cur.execute("TRUNCATE TABLE missions")
    cur.execute("TRUNCATE TABLE telescopes")
    cur.execute("TRUNCATE TABLE moons")
    cur.execute("TRUNCATE TABLE planets")
    cur.execute("TRUNCATE TABLE stars")
    cur.execute("TRUNCATE TABLE star_systems")
    cur.execute("TRUNCATE TABLE constellations")
    cur.execute("TRUNCATE TABLE galaxies")
    cur.execute("SET FOREIGN_KEY_CHECKS=1")

    cur.execute(
        "INSERT INTO galaxies (id,name,galaxy_type,distance_mly) VALUES (1,'Milky Way','Spiral',0.0),(2,'Andromeda','Spiral',2.54)"
    )
    cur.execute(
        "INSERT INTO constellations (id,name,area_sq_deg) VALUES (1,'Orion',594.12),(2,'Lyra',286.48)"
    )
    cur.execute(
        "INSERT INTO star_systems (id,name,galaxy_id,constellation_id,distance_ly) VALUES (1,'Solar System',1,1,0.0),(2,'Vega System',1,2,25.04)"
    )
    cur.execute(
        "INSERT INTO stars (id,name,system_id,spectral_type,mass_solar,radius_solar) VALUES (1,'Sun',1,'G2V',1.0,1.0),(2,'Vega',2,'A0V',2.135,2.362)"
    )
    cur.execute(
        "INSERT INTO planets (id,name,star_id,planet_type,mass_earth,radius_earth,orbit_period_days) VALUES (1,'Earth',1,'Terrestrial',1.0,1.0,365.25),(2,'Mars',1,'Terrestrial',0.107,0.532,687.0),(3,'Vega b',2,'Gas Giant',318.0,11.2,240.0)"
    )
    cur.execute(
        "INSERT INTO moons (id,name,planet_id,mass_lunar,radius_lunar,orbit_period_days) VALUES (1,'Moon',1,1.0,1.0,27.32),(2,'Phobos',2,0.000001,0.017,0.32)"
    )
    cur.execute(
        "INSERT INTO telescopes (id,name,telescope_type,location,aperture_m) VALUES (1,'Hubble','Space','Low Earth Orbit',2.4),(2,'Keck I','Optical','Mauna Kea',10.0)"
    )
    cur.execute(
        "INSERT INTO instruments (id,name,telescope_id,wavelength_band,resolution_arcsec) VALUES (1,'WFC3',1,'UV-Vis',0.04),(2,'HIRES',2,'Optical',0.02)"
    )
    cur.execute(
        "INSERT INTO missions (id,name,agency,start_date,end_date) VALUES (1,'Hubble Mission','NASA','1990-04-24',NULL),(2,'Keck Operations','W. M. Keck','1993-05-01',NULL)"
    )


def generate_observations(cur, target_count: int, batch_size: int = 10_000):
    inserted = 0
    base_time = datetime.utcnow()

    while inserted < target_count:
        remaining = target_count - inserted
        take = batch_size if remaining > batch_size else remaining

        rows = []
        for i in range(take):
            n = inserted + i + 1
            target_type = "star" if n % 2 == 0 else "planet"
            target_id = 1 if target_type == "star" else ((n % 3) + 1)
            obs_at = base_time - timedelta(seconds=(n % 31_536_000))
            rows.append(
                (
                    1 + (n % 2),
                    1 + (n % 2),
                    1 + (n % 2),
                    target_type,
                    target_id,
                    obs_at.strftime("%Y-%m-%d %H:%M:%S"),
                    100 + (n % 5000),
                )
            )

        cur.executemany(
            """
            INSERT INTO observations (telescope_id, instrument_id, mission_id, target_type, target_id, observed_at, exposure_s)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            """,
            rows,
        )
        inserted += take
        if inserted % 100_000 == 0 or inserted == target_count:
            print(f"[MYSQL LOAD] observations: {inserted}/{target_count}")


def load(size: str):
    cfg = SIZE_CONFIG[size]
    with mysql_conn() as conn:
        with conn.cursor() as cur:
            print(f"[MYSQL LOAD] reset + seed for size={size}")
            reset_seed(cur)
            print(f"[MYSQL LOAD] generating observations={cfg['observations']}")
            generate_observations(cur, cfg["observations"])
        conn.commit()
    print(f"[MYSQL LOAD] done size={size}")


def parse_args():
    parser = argparse.ArgumentParser(description="MySQL benchmark runner")
    sub = parser.add_subparsers(dest="command", required=True)

    load_cmd = sub.add_parser("load", help="Generate data for selected size")
    load_cmd.add_argument("--size", choices=["small", "medium", "large"], required=True)

    bench_cmd = sub.add_parser("bench", help="Run benchmark scenarios")
    bench_cmd.add_argument(
        "--size", choices=["small", "medium", "large"], required=True
    )
    bench_cmd.add_argument("--trials", type=int, default=3)

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "load":
        load(args.size)
    else:
        bench_mysql(args.size, args.trials)


if __name__ == "__main__":
    main()
