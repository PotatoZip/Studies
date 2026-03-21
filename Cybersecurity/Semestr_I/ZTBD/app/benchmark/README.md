# Benchmark - prosta instrukcja

1. `benchmark.py` - PostgreSQL
2. `benchmark_mysql.py` - MySQL
3. `benchmark_mongodb.py` - MongoDB
4. `benchmark_neo4j.py` - Neo4j

Kazdy skrypt ma te same 2 komendy:

- `load` - przygotowuje/generuje dane (`small`, `medium`, `large`)
- `bench` - uruchamia benchmark (24 scenariusze CRUD, 3 proby, before/after indexes, zapis wynikow)

## Co oznaczaja foldery z wynikami

- `results/` - pliki CSV z czasami testow
- `results/explain/` - pliki z planami zapytan/profilami (`EXPLAIN`, `PROFILE`)

W skrocie:

- CSV = "ile czasu trwalo"
- EXPLAIN/PROFILE = "dlaczego tyle trwalo"

## Szybki start

1. Uruchom kontenery:

```bash
docker compose up -d
```

2. Wejdz do folderu benchmark i zainstaluj pakiety:

```bash
cd app/benchmark
pip install -r requirements.txt
```

## Komendy dla kazdej bazy

### PostgreSQL

```bash
python benchmark.py load --size small
python benchmark.py bench --size small --trials 3
```

### MySQL

```bash
python benchmark_mysql.py load --size small
python benchmark_mysql.py bench --size small --trials 3
```

### MongoDB

```bash
python benchmark_mongodb.py load --size small
python benchmark_mongodb.py bench --size small --trials 3
```

### Neo4j

```bash
python benchmark_neo4j.py load --size small
python benchmark_neo4j.py bench --size small --trials 3
```

## Rozmiary danych

Dostepne rozmiary:

- `small`
- `medium`
- `large`

## Minimalny workflow

1. Dla kazdej bazy uruchom `load --size small`, potem `bench --size small --trials 3`.
2. To samo powtorz dla `medium`.
3. To samo powtorz dla `large`.
4. Na podstawie CSV robisz tabele i wykresy.
5. Na podstawie plikow z `results/explain` opisujesz roznice planow przed/po indeksach.
