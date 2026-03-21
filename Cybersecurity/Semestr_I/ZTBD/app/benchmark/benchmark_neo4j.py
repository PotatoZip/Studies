import argparse

from neo4j import GraphDatabase

from benchmark_shared import bench_neo4j


SIZE_CONFIG = {
    "small": {"observations": 500_000},
    "medium": {"observations": 1_000_000},
    "large": {"observations": 10_000_000},
}


def driver():
    return GraphDatabase.driver(
        "bolt://localhost:7687", auth=("neo4j", "adminPassword123!")
    )


def load(size: str):
    target = SIZE_CONFIG[size]["observations"]

    with driver() as drv:
        with drv.session() as s:
            s.run("MATCH (n) DETACH DELETE n").consume()

            s.run(
                "CREATE (:Galaxy {id:1, name:'Milky Way', galaxy_type:'Spiral', distance_mly:0.0})"
            ).consume()
            s.run(
                "CREATE (:Galaxy {id:2, name:'Andromeda', galaxy_type:'Spiral', distance_mly:2.54})"
            ).consume()
            s.run(
                "CREATE (:Constellation {id:1, name:'Orion', area_sq_deg:594.12})"
            ).consume()
            s.run(
                "CREATE (:Constellation {id:2, name:'Lyra', area_sq_deg:286.48})"
            ).consume()
            s.run(
                "CREATE (:StarSystem {id:1, name:'Solar System', distance_ly:0.0})"
            ).consume()
            s.run(
                "CREATE (:StarSystem {id:2, name:'Vega System', distance_ly:25.04})"
            ).consume()
            s.run(
                "CREATE (:Star {id:1, name:'Sun', spectral_type:'G2V', mass_solar:1.0, radius_solar:1.0})"
            ).consume()
            s.run(
                "CREATE (:Star {id:2, name:'Vega', spectral_type:'A0V', mass_solar:2.135, radius_solar:2.362})"
            ).consume()
            s.run(
                "CREATE (:Planet {id:1, name:'Earth', planet_type:'Terrestrial', mass_earth:1.0, radius_earth:1.0, orbit_period_days:365.25})"
            ).consume()
            s.run(
                "CREATE (:Planet {id:2, name:'Mars', planet_type:'Terrestrial', mass_earth:0.107, radius_earth:0.532, orbit_period_days:687.0})"
            ).consume()
            s.run(
                "CREATE (:Planet {id:3, name:'Vega b', planet_type:'Gas Giant', mass_earth:318.0, radius_earth:11.2, orbit_period_days:240.0})"
            ).consume()
            s.run(
                "CREATE (:Moon {id:1, name:'Moon', mass_lunar:1.0, radius_lunar:1.0})"
            ).consume()
            s.run(
                "CREATE (:Moon {id:2, name:'Phobos', mass_lunar:0.000001, radius_lunar:0.017})"
            ).consume()
            s.run(
                "CREATE (:Telescope {id:1, name:'Hubble', telescope_type:'Space', location:'Low Earth Orbit', aperture_m:2.4})"
            ).consume()
            s.run(
                "CREATE (:Telescope {id:2, name:'Keck I', telescope_type:'Optical', location:'Mauna Kea', aperture_m:10.0})"
            ).consume()
            s.run(
                "CREATE (:Instrument {id:1, name:'WFC3', wavelength_band:'UV-Vis', resolution_arcsec:0.04})"
            ).consume()
            s.run(
                "CREATE (:Instrument {id:2, name:'HIRES', wavelength_band:'Optical', resolution_arcsec:0.02})"
            ).consume()
            s.run(
                "CREATE (:Mission {id:1, name:'Hubble Mission', agency:'NASA'})"
            ).consume()
            s.run(
                "CREATE (:Mission {id:2, name:'Keck Operations', agency:'W. M. Keck'})"
            ).consume()

            s.run(
                "MATCH (g:Galaxy {id:1}),(ss1:StarSystem {id:1}),(ss2:StarSystem {id:2}) CREATE (g)-[:HAS_SYSTEM]->(ss1), (g)-[:HAS_SYSTEM]->(ss2)"
            ).consume()
            s.run(
                "MATCH (ss1:StarSystem {id:1}),(c1:Constellation {id:1}),(ss2:StarSystem {id:2}),(c2:Constellation {id:2}) CREATE (ss1)-[:IN_CONSTELLATION]->(c1), (ss2)-[:IN_CONSTELLATION]->(c2)"
            ).consume()
            s.run(
                "MATCH (ss1:StarSystem {id:1}),(sun:Star {id:1}),(ss2:StarSystem {id:2}),(vega:Star {id:2}) CREATE (ss1)-[:HAS_STAR]->(sun), (ss2)-[:HAS_STAR]->(vega)"
            ).consume()
            s.run(
                "MATCH (sun:Star {id:1}),(e:Planet {id:1}),(m:Planet {id:2}),(vega:Star {id:2}),(vb:Planet {id:3}) CREATE (sun)-[:HAS_PLANET]->(e), (sun)-[:HAS_PLANET]->(m), (vega)-[:HAS_PLANET]->(vb)"
            ).consume()
            s.run(
                "MATCH (e:Planet {id:1}),(moon:Moon {id:1}),(m:Planet {id:2}),(ph:Moon {id:2}) CREATE (e)-[:HAS_MOON]->(moon), (m)-[:HAS_MOON]->(ph)"
            ).consume()
            s.run(
                "MATCH (t1:Telescope {id:1}),(i1:Instrument {id:1}),(t2:Telescope {id:2}),(i2:Instrument {id:2}) CREATE (t1)-[:HAS_INSTRUMENT]->(i1), (t2)-[:HAS_INSTRUMENT]->(i2)"
            ).consume()

            batch = 10_000
            created = 0
            while created < target:
                take = batch if target - created > batch else target - created
                s.run(
                    """
                    UNWIND range($start, $end) AS n
                    CREATE (o:Observation {
                        id:n,
                        target_type: CASE WHEN n % 2 = 0 THEN 'star' ELSE 'planet' END,
                        target_id: CASE WHEN n % 2 = 0 THEN 1 ELSE 1 + (n % 3) END,
                        mission_id: 1 + (n % 2),
                        observed_at: datetime() - duration({seconds: toInteger(n % 31536000)}),
                        exposure_s: 100 + (n % 5000)
                    })
                    WITH o, n
                    MATCH (i:Instrument {id: 1 + (n % 2)}), (t:Telescope {id: 1 + (n % 2)}), (m:Mission {id: 1 + (n % 2)})
                    CREATE (o)-[:USED_INSTRUMENT]->(i), (o)-[:USED_TELESCOPE]->(t), (o)-[:IN_MISSION]->(m)
                    WITH o, n
                    OPTIONAL MATCH (s:Star {id:1})
                    OPTIONAL MATCH (p:Planet {id: 1 + (n % 3)})
                    FOREACH (_ IN CASE WHEN n % 2 = 0 AND s IS NOT NULL THEN [1] ELSE [] END | CREATE (o)-[:OBSERVED]->(s))
                    FOREACH (_ IN CASE WHEN n % 2 <> 0 AND p IS NOT NULL THEN [1] ELSE [] END | CREATE (o)-[:OBSERVED]->(p))
                    """,
                    start=created + 1,
                    end=created + take,
                ).consume()
                created += take
                if created % 100_000 == 0 or created == target:
                    print(f"[NEO4J LOAD] observations: {created}/{target}")

    print(f"[NEO4J LOAD] done size={size}")


def parse_args():
    parser = argparse.ArgumentParser(description="Neo4j benchmark runner")
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
        bench_neo4j(args.size, args.trials)


if __name__ == "__main__":
    main()
