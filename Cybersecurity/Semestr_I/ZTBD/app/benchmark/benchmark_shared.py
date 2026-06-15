import csv
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pymongo
import pymysql
from neo4j import GraphDatabase


ROOT_DIR = Path(__file__).resolve().parents[2]
RESULTS_DIR = ROOT_DIR / "results"
EXPLAIN_DIR = RESULTS_DIR / "explain"


@dataclass
class Scenario:
    key: str
    operation: str
    description: str


SCENARIOS = [
    Scenario("C1", "CREATE", "Insert single mission"),
    Scenario("C2", "CREATE", "Insert single telescope"),
    Scenario("C3", "CREATE", "Insert single star system"),
    Scenario("C4", "CREATE", "Insert single star"),
    Scenario("C5", "CREATE", "Insert single planet"),
    Scenario("C6", "CREATE", "Insert batch of 100 observations"),
    Scenario("R1", "READ", "Point lookup observation by PK"),
    Scenario("R2", "READ", "Range read by timestamp with limit"),
    Scenario("R3", "READ", "Join-style read across observation context"),
    Scenario("R4", "READ", "Aggregate avg exposure per telescope"),
    Scenario("R5", "READ", "Filter planets by type and mass"),
    Scenario("R6", "READ", "Deep relation read from galaxy"),
    Scenario("U1", "UPDATE", "Update one observation by PK"),
    Scenario("U2", "UPDATE", "Batch update observations by mission"),
    Scenario("U3", "UPDATE", "Batch update planets"),
    Scenario("U4", "UPDATE", "Batch update stars"),
    Scenario("U5", "UPDATE", "Batch update missions"),
    Scenario("U6", "UPDATE", "Batch update instruments"),
    Scenario("D1", "DELETE", "Delete one observation by PK"),
    Scenario("D2", "DELETE", "Delete observations by id range"),
    Scenario("D3", "DELETE", "Delete observations by mission"),
    Scenario("D4", "DELETE", "Delete star-target observations"),
    Scenario("D5", "DELETE", "Delete old observations"),
    Scenario("D6", "DELETE", "Delete low exposure observations"),
]


def now_ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_output_dirs() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    EXPLAIN_DIR.mkdir(parents=True, exist_ok=True)


def write_rows(db_name: str, size: str, rows: List[Dict[str, Any]]) -> Path:
    out_path = RESULTS_DIR / f"{db_name}_benchmark_{size}_{now_ts()}.csv"
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
    return out_path


def save_explain_text(db_name: str, size: str, mode: str, payload: str) -> Path:
    out_path = EXPLAIN_DIR / f"{db_name}_explain_{size}_{mode}_{now_ts()}.txt"
    out_path.write_text(payload, encoding="utf-8")
    return out_path


# ---------------- MySQL ----------------


def mysql_conn():
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3307")),
        user=os.getenv("MYSQL_USER", "admin"),
        password=os.getenv("MYSQL_PASSWORD", "admin"),
        database=os.getenv("MYSQL_DATABASE", "astronomy"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def mysql_index_mode(cur, mode: str) -> None:
    create_sql = [
        "CREATE INDEX idx_observations_observed_at ON observations(observed_at)",
        "CREATE INDEX idx_observations_mission_id ON observations(mission_id)",
        "CREATE INDEX idx_observations_target ON observations(target_type, target_id)",
        "CREATE INDEX idx_observations_telescope_id ON observations(telescope_id)",
        "CREATE INDEX idx_observations_instrument_id ON observations(instrument_id)",
        "CREATE INDEX idx_planets_star_type ON planets(star_id, planet_type)",
        "CREATE INDEX idx_stars_system_id ON stars(system_id)",
        "CREATE INDEX idx_star_systems_galaxy_id ON star_systems(galaxy_id)",
        "CREATE INDEX idx_moons_planet_id ON moons(planet_id)",
        "CREATE INDEX idx_instruments_telescope_id ON instruments(telescope_id)",
    ]
    drop_sql = [
        "DROP INDEX idx_observations_observed_at ON observations",
        "DROP INDEX idx_observations_mission_id ON observations",
        "DROP INDEX idx_observations_target ON observations",
        "DROP INDEX idx_observations_telescope_id ON observations",
        "DROP INDEX idx_observations_instrument_id ON observations",
        "DROP INDEX idx_planets_star_type ON planets",
        "DROP INDEX idx_stars_system_id ON stars",
        "DROP INDEX idx_star_systems_galaxy_id ON star_systems",
        "DROP INDEX idx_moons_planet_id ON moons",
        "DROP INDEX idx_instruments_telescope_id ON instruments",
    ]

    for stmt in drop_sql if mode == "before_indexes" else create_sql:
        try:
            cur.execute(stmt)
        except Exception:
            pass


def mysql_max_ids(cur) -> Dict[str, int]:
    tbls = [
        "observations",
        "missions",
        "stars",
        "planets",
        "star_systems",
        "telescopes",
        "instruments",
    ]
    out = {}
    for t in tbls:
        cur.execute(f"SELECT COALESCE(MAX(id), 1) AS mx FROM {t}")
        out[t] = int(cur.fetchone()["mx"])
    return out


def mysql_exec(cur, key: str, mx: Dict[str, int]) -> None:
    if key == "C1":
        cur.execute(
            "INSERT INTO missions(name, agency, start_date, end_date) VALUES (%s, 'NASA', CURDATE(), NULL)",
            (f"bench-mission-{time.time_ns()}",),
        )
    elif key == "C2":
        cur.execute(
            "INSERT INTO telescopes(name, telescope_type, location, aperture_m) VALUES (%s, 'Optical', 'Benchmark-Location', 8.2)",
            (f"bench-telescope-{time.time_ns()}",),
        )
    elif key == "C3":
        cur.execute(
            "INSERT INTO star_systems(name, galaxy_id, constellation_id, distance_ly) VALUES (%s, 1, 1, 1234.56)",
            (f"bench-system-{time.time_ns()}",),
        )
    elif key == "C4":
        sid = 1 + (time.time_ns() % max(1, mx["star_systems"]))
        cur.execute(
            "INSERT INTO stars(name, system_id, spectral_type, mass_solar, radius_solar) VALUES (%s, %s, 'G2V', 1.001, 0.998)",
            (f"bench-star-{time.time_ns()}", sid),
        )
    elif key == "C5":
        sid = 1 + (time.time_ns() % max(1, mx["stars"]))
        cur.execute(
            "INSERT INTO planets(name, star_id, planet_type, mass_earth, radius_earth, orbit_period_days) VALUES (%s, %s, 'Terrestrial', 1.02, 1.01, 401.5)",
            (f"bench-planet-{time.time_ns()}", sid),
        )
    elif key == "C6":
        cur.execute(
            """
            INSERT INTO observations(telescope_id, instrument_id, mission_id, target_type, target_id, observed_at, exposure_s)
            SELECT
                1 + (gs %% %s),
                1 + (gs %% %s),
                1 + (gs %% %s),
                IF(gs %% 2 = 0, 'star', 'planet'),
                IF(gs %% 2 = 0, 1 + (gs %% %s), 1 + (gs %% %s)),
                NOW() - INTERVAL (gs %% 100000) SECOND,
                100 + (gs %% 5000)
            FROM (
                SELECT 1 gs UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10
            ) a,
            (
                SELECT 0 t UNION ALL SELECT 10 UNION ALL SELECT 20 UNION ALL SELECT 30 UNION ALL SELECT 40 UNION ALL SELECT 50 UNION ALL SELECT 60 UNION ALL SELECT 70 UNION ALL SELECT 80 UNION ALL SELECT 90
            ) b
            """,
            (
                max(1, mx["telescopes"]),
                max(1, mx["instruments"]),
                max(1, mx["missions"]),
                max(1, mx["stars"]),
                max(1, mx["planets"]),
            ),
        )
    elif key == "R1":
        cur.execute(
            "SELECT * FROM observations WHERE id=%s",
            (1 + (time.time_ns() % max(1, mx["observations"])),),
        )
        cur.fetchall()
    elif key == "R2":
        cur.execute(
            "SELECT id, observed_at, exposure_s FROM observations WHERE observed_at >= NOW() - INTERVAL 30 DAY ORDER BY observed_at DESC LIMIT 1000"
        )
        cur.fetchall()
    elif key == "R3":
        cur.execute(
            "SELECT o.id, o.observed_at, i.name instrument_name, t.name telescope_name FROM observations o JOIN instruments i ON i.id=o.instrument_id JOIN telescopes t ON t.id=o.telescope_id WHERE o.mission_id=%s LIMIT 1000",
            (1 + (time.time_ns() % max(1, mx["missions"])),),
        )
        cur.fetchall()
    elif key == "R4":
        cur.execute(
            "SELECT telescope_id, AVG(exposure_s) avg_exposure FROM observations GROUP BY telescope_id ORDER BY avg_exposure DESC LIMIT 100"
        )
        cur.fetchall()
    elif key == "R5":
        cur.execute(
            "SELECT id, name, mass_earth FROM planets WHERE planet_type='Terrestrial' AND mass_earth BETWEEN 0.5 AND 5.0 ORDER BY mass_earth LIMIT 1000"
        )
        cur.fetchall()
    elif key == "R6":
        cur.execute(
            "SELECT g.id, COUNT(o.id) obs_count FROM galaxies g JOIN star_systems ss ON ss.galaxy_id=g.id JOIN stars s ON s.system_id=ss.id JOIN planets p ON p.star_id=s.id LEFT JOIN observations o ON (o.target_type='planet' AND o.target_id=p.id) OR (o.target_type='star' AND o.target_id=s.id) WHERE g.id=1 GROUP BY g.id"
        )
        cur.fetchall()
    elif key == "U1":
        cur.execute(
            "UPDATE observations SET exposure_s=exposure_s+1 WHERE id=%s",
            (1 + (time.time_ns() % max(1, mx["observations"])),),
        )
    elif key == "U2":
        cur.execute(
            "UPDATE observations SET exposure_s=exposure_s+2 WHERE mission_id=%s LIMIT 500",
            (1 + (time.time_ns() % max(1, mx["missions"])),),
        )
    elif key == "U3":
        cur.execute(
            "UPDATE planets SET orbit_period_days=orbit_period_days*1.0001 LIMIT 200"
        )
    elif key == "U4":
        cur.execute("UPDATE stars SET radius_solar=radius_solar*1.0001 LIMIT 200")
    elif key == "U5":
        cur.execute(
            "UPDATE missions SET end_date=CURDATE() WHERE end_date IS NULL LIMIT 100"
        )
    elif key == "U6":
        cur.execute(
            "UPDATE instruments SET resolution_arcsec=resolution_arcsec*0.999 LIMIT 100"
        )
    elif key == "D1":
        cur.execute(
            "DELETE FROM observations WHERE id=%s",
            (1 + (time.time_ns() % max(1, mx["observations"])),),
        )
    elif key == "D2":
        s = 1 + (time.time_ns() % max(1, mx["observations"] - 200))
        cur.execute(
            "DELETE FROM observations WHERE id BETWEEN %s AND %s LIMIT 100",
            (s, s + 1000),
        )
    elif key == "D3":
        cur.execute(
            "DELETE FROM observations WHERE mission_id=%s LIMIT 500",
            (1 + (time.time_ns() % max(1, mx["missions"])),),
        )
    elif key == "D4":
        cur.execute("DELETE FROM observations WHERE target_type='star' LIMIT 500")
    elif key == "D5":
        cur.execute(
            "DELETE FROM observations WHERE observed_at < NOW() - INTERVAL 180 DAY LIMIT 500"
        )
    elif key == "D6":
        cur.execute("DELETE FROM observations WHERE exposure_s < 500 LIMIT 500")


def bench_mysql(size: str, trials: int) -> Tuple[Path, Path, Path]:
    ensure_output_dirs()
    rows: List[Dict[str, Any]] = []
    explain_paths: List[Path] = []

    with mysql_conn() as conn:
        with conn.cursor() as cur:
            for mode in ["before_indexes", "after_indexes"]:
                mysql_index_mode(cur, mode)
                conn.commit()
                mx = mysql_max_ids(cur)
                explain_payload = []

                for sc in SCENARIOS:
                    vals = []
                    for trial in range(1, trials + 1):
                        cur.execute("START TRANSACTION")
                        st = time.perf_counter()
                        mysql_exec(cur, sc.key, mx)
                        ms = (time.perf_counter() - st) * 1000.0
                        cur.execute("ROLLBACK")
                        vals.append(ms)
                        rows.append(
                            {
                                "database": "mysql",
                                "size": size,
                                "index_mode": mode,
                                "scenario": sc.key,
                                "operation": sc.operation,
                                "description": sc.description,
                                "trial": trial,
                                "elapsed_ms": round(ms, 3),
                            }
                        )

                    print(
                        f"[MYSQL] {mode} | {sc.key} {sc.operation:<6} | avg={sum(vals)/len(vals):10.3f} ms"
                    )

                    if sc.operation == "READ":
                        try:
                            plan_q = "EXPLAIN FORMAT=JSON SELECT * FROM observations WHERE id=1"
                            if sc.key == "R2":
                                plan_q = "EXPLAIN FORMAT=JSON SELECT id, observed_at, exposure_s FROM observations WHERE observed_at >= NOW() - INTERVAL 30 DAY ORDER BY observed_at DESC LIMIT 1000"
                            elif sc.key == "R3":
                                plan_q = "EXPLAIN FORMAT=JSON SELECT o.id, o.observed_at, i.name, t.name FROM observations o JOIN instruments i ON i.id=o.instrument_id JOIN telescopes t ON t.id=o.telescope_id WHERE o.mission_id=1 LIMIT 1000"
                            elif sc.key == "R4":
                                plan_q = "EXPLAIN FORMAT=JSON SELECT telescope_id, AVG(exposure_s) FROM observations GROUP BY telescope_id ORDER BY AVG(exposure_s) DESC LIMIT 100"
                            elif sc.key == "R5":
                                plan_q = "EXPLAIN FORMAT=JSON SELECT id, name, mass_earth FROM planets WHERE planet_type='Terrestrial' AND mass_earth BETWEEN 0.5 AND 5.0 ORDER BY mass_earth LIMIT 1000"
                            elif sc.key == "R6":
                                plan_q = "EXPLAIN FORMAT=JSON SELECT g.id, COUNT(o.id) FROM galaxies g JOIN star_systems ss ON ss.galaxy_id=g.id JOIN stars s ON s.system_id=ss.id JOIN planets p ON p.star_id=s.id LEFT JOIN observations o ON (o.target_type='planet' AND o.target_id=p.id) OR (o.target_type='star' AND o.target_id=s.id) WHERE g.id=1 GROUP BY g.id"

                            cur.execute(plan_q)
                            explain_payload.append(
                                f"\n=== {sc.key} | {sc.description} ===\n{json.dumps(cur.fetchone(), ensure_ascii=False, indent=2)}"
                            )
                        except Exception as ex:
                            explain_payload.append(
                                f"\n=== {sc.key} | {sc.description} ===\nEXPLAIN failed: {ex}"
                            )

                explain_paths.append(
                    save_explain_text("mysql", size, mode, "\n".join(explain_payload))
                )

    csv_path = write_rows("mysql", size, rows)
    return csv_path, explain_paths[0], explain_paths[1]


# ---------------- MongoDB ----------------


def mongo_db():
    client = pymongo.MongoClient(
        host=os.getenv("MONGO_HOST", "localhost"),
        port=int(os.getenv("MONGO_PORT", "27017")),
        username=os.getenv("MONGO_USER", "admin"),
        password=os.getenv("MONGO_PASSWORD", "admin"),
        authSource=os.getenv("MONGO_AUTHSOURCE", "admin"),
    )
    return client[os.getenv("MONGO_DATABASE", "astronomy")]


def mongo_index_mode(db, mode: str) -> None:
    idx_defs = [
        (
            "observations",
            [("observed_at", pymongo.DESCENDING)],
            "idx_observations_observed_at",
        ),
        (
            "observations",
            [("mission_id", pymongo.ASCENDING)],
            "idx_observations_mission_id",
        ),
        (
            "observations",
            [("target_type", pymongo.ASCENDING), ("target_id", pymongo.ASCENDING)],
            "idx_observations_target",
        ),
        (
            "observations",
            [("telescope_id", pymongo.ASCENDING)],
            "idx_observations_telescope_id",
        ),
        (
            "observations",
            [("instrument_id", pymongo.ASCENDING)],
            "idx_observations_instrument_id",
        ),
        (
            "planets",
            [("star_id", pymongo.ASCENDING), ("planet_type", pymongo.ASCENDING)],
            "idx_planets_star_type",
        ),
    ]
    for coll, fields, name in idx_defs:
        try:
            if mode == "before_indexes":
                db[coll].drop_index(name)
            else:
                db[coll].create_index(fields, name=name)
        except Exception:
            pass


def mongo_max_ids(db) -> Dict[str, int]:
    def max_id(coll: str) -> int:
        doc = db[coll].find_one(sort=[("_id", -1)])
        return int(doc["_id"]) if doc and isinstance(doc.get("_id"), int) else 1

    return {
        "observations": max_id("observations"),
        "missions": max_id("missions"),
        "stars": max_id("stars"),
        "planets": max_id("planets"),
        "star_systems": max_id("star_systems"),
        "telescopes": max_id("telescopes"),
        "instruments": max_id("instruments"),
    }


def mongo_exec(db, key: str, mx: Dict[str, int]) -> None:
    obs = db["observations"]
    missions = db["missions"]
    telescopes = db["telescopes"]
    stars = db["stars"]
    planets = db["planets"]
    instruments = db["instruments"]

    if key == "C1":
        missions.insert_one(
            {
                "_id": int(time.time_ns() % 2_000_000_000),
                "name": f"bench-mission-{time.time_ns()}",
                "agency": "NASA",
                "start_date": datetime.now(UTC),
                "end_date": None,
            }
        )
    elif key == "C2":
        telescopes.insert_one(
            {
                "_id": int(time.time_ns() % 2_000_000_000),
                "name": f"bench-telescope-{time.time_ns()}",
                "telescope_type": "Optical",
                "location": "Benchmark-Location",
                "aperture_m": 8.2,
            }
        )
    elif key == "C3":
        db["star_systems"].insert_one(
            {
                "_id": int(time.time_ns() % 2_000_000_000),
                "name": f"bench-system-{time.time_ns()}",
                "galaxy_id": 1,
                "constellation_id": 1,
                "distance_ly": 1234.56,
            }
        )
    elif key == "C4":
        sid = 1 + (time.time_ns() % max(1, mx["star_systems"]))
        stars.insert_one(
            {
                "_id": int(time.time_ns() % 2_000_000_000),
                "name": f"bench-star-{time.time_ns()}",
                "system_id": int(sid),
                "spectral_type": "G2V",
                "mass_solar": 1.001,
                "radius_solar": 0.998,
            }
        )
    elif key == "C5":
        sid = 1 + (time.time_ns() % max(1, mx["stars"]))
        planets.insert_one(
            {
                "_id": int(time.time_ns() % 2_000_000_000),
                "name": f"bench-planet-{time.time_ns()}",
                "star_id": int(sid),
                "planet_type": "Terrestrial",
                "mass_earth": 1.02,
                "radius_earth": 1.01,
                "orbit_period_days": 401.5,
            }
        )
    elif key == "C6":
        docs = []
        for i in range(100):
            docs.append(
                {
                    "_id": int((time.time_ns() + i) % 2_000_000_000),
                    "telescope_id": 1 + (i % max(1, mx["telescopes"])),
                    "instrument_id": 1 + (i % max(1, mx["instruments"])),
                    "mission_id": 1 + (i % max(1, mx["missions"])),
                    "target_type": "star" if i % 2 == 0 else "planet",
                    "target_id": 1 + (i % max(1, mx["stars"])),
                    "observed_at": datetime.now(UTC),
                    "exposure_s": 100 + i,
                }
            )
        obs.insert_many(docs, ordered=False)
    elif key == "R1":
        _ = obs.find_one({"_id": 1 + (time.time_ns() % max(1, mx["observations"]))})
    elif key == "R2":
        _ = list(
            obs.find({"observed_at": {"$gte": datetime.now(UTC)}})
            .sort("observed_at", -1)
            .limit(1000)
        )
    elif key == "R3":
        _ = list(
            obs.aggregate(
                [
                    {
                        "$lookup": {
                            "from": "instruments",
                            "localField": "instrument_id",
                            "foreignField": "_id",
                            "as": "inst",
                        }
                    },
                    {
                        "$lookup": {
                            "from": "telescopes",
                            "localField": "telescope_id",
                            "foreignField": "_id",
                            "as": "tel",
                        }
                    },
                    {"$limit": 1000},
                ]
            )
        )
    elif key == "R4":
        _ = list(
            obs.aggregate(
                [
                    {
                        "$group": {
                            "_id": "$telescope_id",
                            "avg_exposure": {"$avg": "$exposure_s"},
                        }
                    },
                    {"$sort": {"avg_exposure": -1}},
                    {"$limit": 100},
                ]
            )
        )
    elif key == "R5":
        _ = list(
            planets.find(
                {"planet_type": "Terrestrial", "mass_earth": {"$gte": 0.5, "$lte": 5.0}}
            )
            .sort("mass_earth", 1)
            .limit(1000)
        )
    elif key == "R6":
        _ = list(
            db["galaxies"].aggregate(
                [
                    {"$match": {"_id": 1}},
                    {
                        "$lookup": {
                            "from": "star_systems",
                            "localField": "_id",
                            "foreignField": "galaxy_id",
                            "as": "systems",
                        }
                    },
                ]
            )
        )
    elif key == "U1":
        obs.update_one(
            {"_id": 1 + (time.time_ns() % max(1, mx["observations"]))},
            {"$inc": {"exposure_s": 1}},
        )
    elif key == "U2":
        ids = [
            d["_id"]
            for d in obs.find(
                {"mission_id": 1 + (time.time_ns() % max(1, mx["missions"]))},
                {"_id": 1},
            ).limit(500)
        ]
        if ids:
            obs.update_many({"_id": {"$in": ids}}, {"$inc": {"exposure_s": 2}})
    elif key == "U3":
        ids = [d["_id"] for d in planets.find({}, {"_id": 1}).limit(200)]
        if ids:
            planets.update_many(
                {"_id": {"$in": ids}}, {"$mul": {"orbit_period_days": 1.0001}}
            )
    elif key == "U4":
        ids = [d["_id"] for d in stars.find({}, {"_id": 1}).limit(200)]
        if ids:
            stars.update_many({"_id": {"$in": ids}}, {"$mul": {"radius_solar": 1.0001}})
    elif key == "U5":
        ids = [
            d["_id"] for d in missions.find({"end_date": None}, {"_id": 1}).limit(100)
        ]
        if ids:
            missions.update_many(
                {"_id": {"$in": ids}}, {"$set": {"end_date": datetime.now(UTC)}}
            )
    elif key == "U6":
        ids = [d["_id"] for d in instruments.find({}, {"_id": 1}).limit(100)]
        if ids:
            instruments.update_many(
                {"_id": {"$in": ids}}, {"$mul": {"resolution_arcsec": 0.999}}
            )
    elif key == "D1":
        obs.delete_one({"_id": 1 + (time.time_ns() % max(1, mx["observations"]))})
    elif key == "D2":
        s = 1 + (time.time_ns() % max(1, mx["observations"] - 200))
        ids = [
            d["_id"]
            for d in obs.find(
                {"_id": {"$gte": int(s), "$lte": int(s + 1000)}}, {"_id": 1}
            ).limit(100)
        ]
        if ids:
            obs.delete_many({"_id": {"$in": ids}})
    elif key == "D3":
        ids = [
            d["_id"]
            for d in obs.find(
                {"mission_id": 1 + (time.time_ns() % max(1, mx["missions"]))},
                {"_id": 1},
            ).limit(500)
        ]
        if ids:
            obs.delete_many({"_id": {"$in": ids}})
    elif key == "D4":
        ids = [
            d["_id"] for d in obs.find({"target_type": "star"}, {"_id": 1}).limit(500)
        ]
        if ids:
            obs.delete_many({"_id": {"$in": ids}})
    elif key == "D5":
        ids = [d["_id"] for d in obs.find({}, {"_id": 1}).limit(500)]
        if ids:
            obs.delete_many({"_id": {"$in": ids}})
    elif key == "D6":
        ids = [
            d["_id"]
            for d in obs.find({"exposure_s": {"$lt": 500}}, {"_id": 1}).limit(500)
        ]
        if ids:
            obs.delete_many({"_id": {"$in": ids}})


def bench_mongodb(size: str, trials: int) -> Tuple[Path, Path, Path]:
    ensure_output_dirs()
    db = mongo_db()
    rows: List[Dict[str, Any]] = []
    explain_paths: List[Path] = []

    for mode in ["before_indexes", "after_indexes"]:
        mongo_index_mode(db, mode)
        mx = mongo_max_ids(db)
        explain_payload = []

        for sc in SCENARIOS:
            vals = []
            for trial in range(1, trials + 1):
                st = time.perf_counter()
                mongo_exec(db, sc.key, mx)
                ms = (time.perf_counter() - st) * 1000.0
                vals.append(ms)
                rows.append(
                    {
                        "database": "mongodb",
                        "size": size,
                        "index_mode": mode,
                        "scenario": sc.key,
                        "operation": sc.operation,
                        "description": sc.description,
                        "trial": trial,
                        "elapsed_ms": round(ms, 3),
                    }
                )

            print(
                f"[MONGODB] {mode} | {sc.key} {sc.operation:<6} | avg={sum(vals)/len(vals):10.3f} ms"
            )

            if sc.operation == "READ":
                try:
                    if sc.key == "R1":
                        plan = db["observations"].find({"_id": 1}).explain()
                    elif sc.key == "R2":
                        plan = (
                            db["observations"]
                            .find({"observed_at": {"$gte": datetime.now(UTC)}})
                            .sort("observed_at", -1)
                            .limit(1000)
                            .explain()
                        )
                    elif sc.key == "R3":
                        plan = db.command(
                            "aggregate",
                            "observations",
                            pipeline=[
                                {
                                    "$lookup": {
                                        "from": "instruments",
                                        "localField": "instrument_id",
                                        "foreignField": "_id",
                                        "as": "inst",
                                    }
                                },
                                {"$limit": 1000},
                            ],
                            cursor={},
                            explain=True,
                        )
                    elif sc.key == "R4":
                        plan = db.command(
                            "aggregate",
                            "observations",
                            pipeline=[
                                {
                                    "$group": {
                                        "_id": "$telescope_id",
                                        "avg_exposure": {"$avg": "$exposure_s"},
                                    }
                                }
                            ],
                            cursor={},
                            explain=True,
                        )
                    elif sc.key == "R5":
                        plan = (
                            db["planets"]
                            .find(
                                {
                                    "planet_type": "Terrestrial",
                                    "mass_earth": {"$gte": 0.5, "$lte": 5.0},
                                }
                            )
                            .explain()
                        )
                    else:
                        plan = db.command(
                            "aggregate",
                            "galaxies",
                            pipeline=[
                                {"$match": {"_id": 1}},
                                {
                                    "$lookup": {
                                        "from": "star_systems",
                                        "localField": "_id",
                                        "foreignField": "galaxy_id",
                                        "as": "systems",
                                    }
                                },
                            ],
                            cursor={},
                            explain=True,
                        )
                    explain_payload.append(
                        f"\n=== {sc.key} | {sc.description} ===\n{json.dumps(plan, default=str, ensure_ascii=False, indent=2)}"
                    )
                except Exception as ex:
                    explain_payload.append(
                        f"\n=== {sc.key} | {sc.description} ===\nEXPLAIN failed: {ex}"
                    )

        explain_paths.append(
            save_explain_text("mongodb", size, mode, "\n".join(explain_payload))
        )

    csv_path = write_rows("mongodb", size, rows)
    return csv_path, explain_paths[0], explain_paths[1]


# ---------------- Neo4j ----------------


def neo4j_driver():
    return GraphDatabase.driver(
        os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        auth=(
            os.getenv("NEO4J_USER", "neo4j"),
            os.getenv("NEO4J_PASSWORD", "adminPassword123!"),
        ),
    )


def neo4j_index_mode(session, mode: str) -> None:
    create_stmts = [
        "CREATE INDEX idx_obs_observed_at IF NOT EXISTS FOR (o:Observation) ON (o.observed_at)",
        "CREATE INDEX idx_obs_target IF NOT EXISTS FOR (o:Observation) ON (o.target_type, o.target_id)",
        "CREATE INDEX idx_obs_mission IF NOT EXISTS FOR (o:Observation) ON (o.mission_id)",
    ]
    drop_stmts = [
        "DROP INDEX idx_obs_observed_at IF EXISTS",
        "DROP INDEX idx_obs_target IF EXISTS",
        "DROP INDEX idx_obs_mission IF EXISTS",
    ]
    for stmt in drop_stmts if mode == "before_indexes" else create_stmts:
        try:
            session.run(stmt).consume()
        except Exception:
            pass


def neo4j_exec(tx, key: str) -> None:
    if key == "C1":
        tx.run(
            "CREATE (:Mission {id:$id, name:$name, agency:'NASA'})",
            id=int(time.time_ns() % 2_000_000_000),
            name=f"bench-mission-{time.time_ns()}",
        )
    elif key == "C2":
        tx.run(
            "CREATE (:Telescope {id:$id, name:$name, telescope_type:'Optical', location:'Benchmark-Location', aperture_m:8.2})",
            id=int(time.time_ns() % 2_000_000_000),
            name=f"bench-telescope-{time.time_ns()}",
        )
    elif key == "C3":
        tx.run(
            "CREATE (:StarSystem {id:$id, name:$name, distance_ly:1234.56})",
            id=int(time.time_ns() % 2_000_000_000),
            name=f"bench-system-{time.time_ns()}",
        )
    elif key == "C4":
        tx.run(
            "CREATE (:Star {id:$id, name:$name, spectral_type:'G2V', mass_solar:1.001, radius_solar:0.998})",
            id=int(time.time_ns() % 2_000_000_000),
            name=f"bench-star-{time.time_ns()}",
        )
    elif key == "C5":
        tx.run(
            "CREATE (:Planet {id:$id, name:$name, planet_type:'Terrestrial', mass_earth:1.02, radius_earth:1.01, orbit_period_days:401.5})",
            id=int(time.time_ns() % 2_000_000_000),
            name=f"bench-planet-{time.time_ns()}",
        )
    elif key == "C6":
        tx.run(
            "UNWIND range(1,100) AS i CREATE (:Observation {id:toInteger(rand()*2000000000), target_type:CASE WHEN i % 2 = 0 THEN 'star' ELSE 'planet' END, target_id:i, observed_at:datetime(), exposure_s:100+i})"
        )
    elif key == "R1":
        list(tx.run("MATCH (o:Observation {id:1}) RETURN o"))
    elif key == "R2":
        list(
            tx.run(
                "MATCH (o:Observation) WHERE o.observed_at >= datetime() - duration('P30D') RETURN o.id, o.observed_at, o.exposure_s ORDER BY o.observed_at DESC LIMIT 1000"
            )
        )
    elif key == "R3":
        list(
            tx.run(
                "MATCH (o:Observation)-[:USED_INSTRUMENT]->(i:Instrument), (o)-[:USED_TELESCOPE]->(t:Telescope) RETURN o.id, i.name, t.name LIMIT 1000"
            )
        )
    elif key == "R4":
        list(
            tx.run(
                "MATCH (o:Observation) RETURN o.target_id AS telescope_id, avg(o.exposure_s) AS avg_exposure ORDER BY avg_exposure DESC LIMIT 100"
            )
        )
    elif key == "R5":
        list(
            tx.run(
                "MATCH (p:Planet) WHERE p.planet_type='Terrestrial' AND p.mass_earth >= 0.5 AND p.mass_earth <= 5.0 RETURN p.id, p.name, p.mass_earth ORDER BY p.mass_earth LIMIT 1000"
            )
        )
    elif key == "R6":
        list(
            tx.run(
                "MATCH (g:Galaxy {id:1})-[:HAS_SYSTEM]->(:StarSystem)-[:HAS_STAR]->(s:Star) OPTIONAL MATCH (o:Observation)-[:OBSERVED]->(s) RETURN g.id, count(o) AS obs_count"
            )
        )
    elif key == "U1":
        tx.run(
            "MATCH (o:Observation {id:1}) SET o.exposure_s = coalesce(o.exposure_s,0) + 1"
        )
    elif key == "U2":
        tx.run(
            "MATCH (o:Observation) WITH o LIMIT 500 SET o.exposure_s = coalesce(o.exposure_s,0) + 2"
        )
    elif key == "U3":
        tx.run(
            "MATCH (p:Planet) WITH p LIMIT 200 SET p.orbit_period_days = coalesce(p.orbit_period_days,1) * 1.0001"
        )
    elif key == "U4":
        tx.run(
            "MATCH (s:Star) WITH s LIMIT 200 SET s.radius_solar = coalesce(s.radius_solar,1) * 1.0001"
        )
    elif key == "U5":
        tx.run("MATCH (m:Mission) WITH m LIMIT 100 SET m.end_date = date()")
    elif key == "U6":
        tx.run(
            "MATCH (i:Instrument) WITH i LIMIT 100 SET i.resolution_arcsec = coalesce(i.resolution_arcsec,1) * 0.999"
        )
    elif key == "D1":
        tx.run("MATCH (o:Observation {id:1}) DETACH DELETE o")
    elif key == "D2":
        tx.run("MATCH (o:Observation) WITH o LIMIT 100 DETACH DELETE o")
    elif key == "D3":
        tx.run(
            "MATCH (o:Observation)-[:IN_MISSION]->(:Mission) WITH o LIMIT 500 DETACH DELETE o"
        )
    elif key == "D4":
        tx.run(
            "MATCH (o:Observation {target_type:'star'}) WITH o LIMIT 500 DETACH DELETE o"
        )
    elif key == "D5":
        tx.run(
            "MATCH (o:Observation) WHERE o.exposure_s IS NOT NULL WITH o LIMIT 500 DETACH DELETE o"
        )
    elif key == "D6":
        tx.run(
            "MATCH (o:Observation) WHERE o.exposure_s < 500 WITH o LIMIT 500 DETACH DELETE o"
        )


def bench_neo4j(size: str, trials: int) -> Tuple[Path, Path, Path]:
    ensure_output_dirs()
    rows: List[Dict[str, Any]] = []
    explain_paths: List[Path] = []

    driver = neo4j_driver()
    try:
        with driver.session() as session:
            for mode in ["before_indexes", "after_indexes"]:
                neo4j_index_mode(session, mode)
                explain_payload = []

                for sc in SCENARIOS:
                    vals = []
                    for trial in range(1, trials + 1):
                        with session.begin_transaction() as tx:
                            st = time.perf_counter()
                            neo4j_exec(tx, sc.key)
                            ms = (time.perf_counter() - st) * 1000.0
                            tx.rollback()
                        vals.append(ms)
                        rows.append(
                            {
                                "database": "neo4j",
                                "size": size,
                                "index_mode": mode,
                                "scenario": sc.key,
                                "operation": sc.operation,
                                "description": sc.description,
                                "trial": trial,
                                "elapsed_ms": round(ms, 3),
                            }
                        )

                    print(
                        f"[NEO4J] {mode} | {sc.key} {sc.operation:<6} | avg={sum(vals)/len(vals):10.3f} ms"
                    )

                    if sc.operation == "READ":
                        try:
                            q = "PROFILE MATCH (o:Observation {id:1}) RETURN o"
                            if sc.key == "R2":
                                q = "PROFILE MATCH (o:Observation) WHERE o.observed_at >= datetime() - duration('P30D') RETURN o.id, o.observed_at, o.exposure_s ORDER BY o.observed_at DESC LIMIT 1000"
                            elif sc.key == "R3":
                                q = "PROFILE MATCH (o:Observation)-[:USED_INSTRUMENT]->(i:Instrument), (o)-[:USED_TELESCOPE]->(t:Telescope) RETURN o.id, i.name, t.name LIMIT 1000"
                            elif sc.key == "R4":
                                q = "PROFILE MATCH (o:Observation) RETURN o.target_id AS telescope_id, avg(o.exposure_s) AS avg_exposure ORDER BY avg_exposure DESC LIMIT 100"
                            elif sc.key == "R5":
                                q = "PROFILE MATCH (p:Planet) WHERE p.planet_type='Terrestrial' AND p.mass_earth >= 0.5 AND p.mass_earth <= 5.0 RETURN p.id, p.name, p.mass_earth ORDER BY p.mass_earth LIMIT 1000"
                            elif sc.key == "R6":
                                q = "PROFILE MATCH (g:Galaxy {id:1})-[:HAS_SYSTEM]->(:StarSystem)-[:HAS_STAR]->(s:Star) OPTIONAL MATCH (o:Observation)-[:OBSERVED]->(s) RETURN g.id, count(o) AS obs_count"

                            summary = session.run(q).consume()
                            explain_payload.append(
                                f"\n=== {sc.key} | {sc.description} ===\n{summary.profile}"
                            )
                        except Exception as ex:
                            explain_payload.append(
                                f"\n=== {sc.key} | {sc.description} ===\nPROFILE failed: {ex}"
                            )

                explain_paths.append(
                    save_explain_text("neo4j", size, mode, "\n".join(explain_payload))
                )
    finally:
        driver.close()

    csv_path = write_rows("neo4j", size, rows)
    return csv_path, explain_paths[0], explain_paths[1]
