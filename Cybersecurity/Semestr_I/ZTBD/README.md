# ZTBD - Astronomy databases benchmark

This project compares two relational databases (PostgreSQL, MySQL) and two non-relational databases (MongoDB, Neo4j) using an astronomy dataset.

## Structure

- `docker-compose.yml` - database services
- `app/` - initialization and benchmark scripts
- `results/` - benchmark outputs (CSV)

## Quick start

1. Start databases:
   - `docker compose up -d`
2. Load data and run benchmarks:
   - `cd app/benchmark`
   - `python benchmark.py load --size small`
   - `python benchmark.py bench --size small`

## Data model

Relational schema includes at least 10 tables: galaxies, constellations, star_systems, stars, planets, moons, telescopes, instruments, missions, observations.

MongoDB stores star systems with embedded stars/planets/moons and separate collections for telescopes, missions, and observations.

Neo4j stores the same entities as nodes with relationships between systems, stars, planets, moons, telescopes, instruments, missions, and observations.
