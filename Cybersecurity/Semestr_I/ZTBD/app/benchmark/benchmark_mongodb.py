import argparse
from datetime import datetime, timedelta

import pymongo

from benchmark_shared import bench_mongodb


SIZE_CONFIG = {
    "small": {"observations": 500_000},
    "medium": {"observations": 1_000_000},
    "large": {"observations": 10_000_000},
}


def get_db():
    client = pymongo.MongoClient(
        host="localhost",
        port=27017,
        username="admin",
        password="admin",
        authSource="admin",
    )
    return client["astronomy"]


def load(size: str):
    cfg = SIZE_CONFIG[size]
    db = get_db()
    db.client.drop_database("astronomy")
    db = get_db()

    db.galaxies.insert_many(
        [
            {
                "_id": 1,
                "name": "Milky Way",
                "galaxy_type": "Spiral",
                "distance_mly": 0.0,
            },
            {
                "_id": 2,
                "name": "Andromeda",
                "galaxy_type": "Spiral",
                "distance_mly": 2.54,
            },
        ]
    )
    db.constellations.insert_many(
        [
            {"_id": 1, "name": "Orion", "area_sq_deg": 594.12},
            {"_id": 2, "name": "Lyra", "area_sq_deg": 286.48},
        ]
    )
    db.star_systems.insert_many(
        [
            {
                "_id": 1,
                "name": "Solar System",
                "galaxy_id": 1,
                "constellation_id": 1,
                "distance_ly": 0.0,
            },
            {
                "_id": 2,
                "name": "Vega System",
                "galaxy_id": 1,
                "constellation_id": 2,
                "distance_ly": 25.04,
            },
        ]
    )
    db.stars.insert_many(
        [
            {
                "_id": 1,
                "name": "Sun",
                "system_id": 1,
                "spectral_type": "G2V",
                "mass_solar": 1.0,
                "radius_solar": 1.0,
            },
            {
                "_id": 2,
                "name": "Vega",
                "system_id": 2,
                "spectral_type": "A0V",
                "mass_solar": 2.135,
                "radius_solar": 2.362,
            },
        ]
    )
    db.planets.insert_many(
        [
            {
                "_id": 1,
                "name": "Earth",
                "star_id": 1,
                "planet_type": "Terrestrial",
                "mass_earth": 1.0,
                "radius_earth": 1.0,
                "orbit_period_days": 365.25,
            },
            {
                "_id": 2,
                "name": "Mars",
                "star_id": 1,
                "planet_type": "Terrestrial",
                "mass_earth": 0.107,
                "radius_earth": 0.532,
                "orbit_period_days": 687.0,
            },
            {
                "_id": 3,
                "name": "Vega b",
                "star_id": 2,
                "planet_type": "Gas Giant",
                "mass_earth": 318.0,
                "radius_earth": 11.2,
                "orbit_period_days": 240.0,
            },
        ]
    )
    db.moons.insert_many(
        [
            {
                "_id": 1,
                "name": "Moon",
                "planet_id": 1,
                "mass_lunar": 1.0,
                "radius_lunar": 1.0,
                "orbit_period_days": 27.3,
            },
            {
                "_id": 2,
                "name": "Phobos",
                "planet_id": 2,
                "mass_lunar": 0.000001,
                "radius_lunar": 0.017,
                "orbit_period_days": 0.32,
            },
        ]
    )
    db.telescopes.insert_many(
        [
            {
                "_id": 1,
                "name": "Hubble",
                "telescope_type": "Space",
                "location": "Low Earth Orbit",
                "aperture_m": 2.4,
            },
            {
                "_id": 2,
                "name": "Keck I",
                "telescope_type": "Optical",
                "location": "Mauna Kea",
                "aperture_m": 10.0,
            },
        ]
    )
    db.instruments.insert_many(
        [
            {
                "_id": 1,
                "name": "WFC3",
                "telescope_id": 1,
                "wavelength_band": "UV-Vis",
                "resolution_arcsec": 0.04,
            },
            {
                "_id": 2,
                "name": "HIRES",
                "telescope_id": 2,
                "wavelength_band": "Optical",
                "resolution_arcsec": 0.02,
            },
        ]
    )
    db.missions.insert_many(
        [
            {
                "_id": 1,
                "name": "Hubble Mission",
                "agency": "NASA",
                "start_date": datetime(1990, 4, 24),
                "end_date": None,
            },
            {
                "_id": 2,
                "name": "Keck Operations",
                "agency": "W. M. Keck",
                "start_date": datetime(1993, 5, 1),
                "end_date": None,
            },
        ]
    )

    target = cfg["observations"]
    batch = 10_000
    inserted = 0
    base_time = datetime.utcnow()

    while inserted < target:
        take = batch if target - inserted > batch else target - inserted
        docs = []
        for i in range(take):
            n = inserted + i + 1
            ttype = "star" if n % 2 == 0 else "planet"
            tid = 1 if ttype == "star" else ((n % 3) + 1)
            docs.append(
                {
                    "_id": n,
                    "telescope_id": 1 + (n % 2),
                    "instrument_id": 1 + (n % 2),
                    "mission_id": 1 + (n % 2),
                    "target_type": ttype,
                    "target_id": tid,
                    "observed_at": base_time - timedelta(seconds=(n % 31_536_000)),
                    "exposure_s": 100 + (n % 5000),
                }
            )
        db.observations.insert_many(docs, ordered=False)
        inserted += take
        if inserted % 100_000 == 0 or inserted == target:
            print(f"[MONGO LOAD] observations: {inserted}/{target}")

    print(f"[MONGO LOAD] done size={size}")


def parse_args():
    parser = argparse.ArgumentParser(description="MongoDB benchmark runner")
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
        bench_mongodb(args.size, args.trials)


if __name__ == "__main__":
    main()
