# Diagramy architektury baz danych

## 1) ERD - PostgreSQL

```mermaid
erDiagram
    GALAXIES {
        INT id PK
        VARCHAR name UK
        VARCHAR galaxy_type
        NUMERIC distance_mly
    }

    CONSTELLATIONS {
        INT id PK
        VARCHAR name UK
        NUMERIC area_sq_deg
    }

    STAR_SYSTEMS {
        INT id PK
        VARCHAR name UK
        INT galaxy_id FK
        INT constellation_id FK
        NUMERIC distance_ly
    }

    STARS {
        INT id PK
        VARCHAR name UK
        INT system_id FK
        VARCHAR spectral_type
        NUMERIC mass_solar
        NUMERIC radius_solar
    }

    PLANETS {
        INT id PK
        VARCHAR name
        INT star_id FK
        VARCHAR planet_type
        NUMERIC mass_earth
        NUMERIC radius_earth
        NUMERIC orbit_period_days
    }

    MOONS {
        INT id PK
        VARCHAR name
        INT planet_id FK
        NUMERIC mass_lunar
        NUMERIC radius_lunar
        NUMERIC orbit_period_days
    }

    TELESCOPES {
        INT id PK
        VARCHAR name UK
        VARCHAR telescope_type
        VARCHAR location
        NUMERIC aperture_m
    }

    INSTRUMENTS {
        INT id PK
        VARCHAR name
        INT telescope_id FK
        VARCHAR wavelength_band
        NUMERIC resolution_arcsec
    }

    MISSIONS {
        INT id PK
        VARCHAR name UK
        VARCHAR agency
        DATE start_date
        DATE end_date
    }

    OBSERVATIONS {
        INT id PK
        INT telescope_id FK
        INT instrument_id FK
        INT mission_id FK
        VARCHAR target_type
        INT target_id
        TIMESTAMP observed_at
        INT exposure_s
    }

    GALAXIES ||--o{ STAR_SYSTEMS : contains
    CONSTELLATIONS ||--o{ STAR_SYSTEMS : maps
    STAR_SYSTEMS ||--o{ STARS : has
    STARS ||--o{ PLANETS : has
    PLANETS ||--o{ MOONS : has
    TELESCOPES ||--o{ INSTRUMENTS : has
    TELESCOPES ||--o{ OBSERVATIONS : used_in
    INSTRUMENTS ||--o{ OBSERVATIONS : used_in
    MISSIONS ||--o{ OBSERVATIONS : context
```

## 2) ERD - MySQL

```mermaid
erDiagram
    GALAXIES {
        INT id PK
        VARCHAR name UK
        VARCHAR galaxy_type
        DECIMAL distance_mly
    }

    CONSTELLATIONS {
        INT id PK
        VARCHAR name UK
        DECIMAL area_sq_deg
    }

    STAR_SYSTEMS {
        INT id PK
        VARCHAR name UK
        INT galaxy_id FK
        INT constellation_id FK
        DECIMAL distance_ly
    }

    STARS {
        INT id PK
        VARCHAR name UK
        INT system_id FK
        VARCHAR spectral_type
        DECIMAL mass_solar
        DECIMAL radius_solar
    }

    PLANETS {
        INT id PK
        VARCHAR name
        INT star_id FK
        VARCHAR planet_type
        DECIMAL mass_earth
        DECIMAL radius_earth
        DECIMAL orbit_period_days
    }

    MOONS {
        INT id PK
        VARCHAR name
        INT planet_id FK
        DECIMAL mass_lunar
        DECIMAL radius_lunar
        DECIMAL orbit_period_days
    }

    TELESCOPES {
        INT id PK
        VARCHAR name UK
        VARCHAR telescope_type
        VARCHAR location
        DECIMAL aperture_m
    }

    INSTRUMENTS {
        INT id PK
        VARCHAR name
        INT telescope_id FK
        VARCHAR wavelength_band
        DECIMAL resolution_arcsec
    }

    MISSIONS {
        INT id PK
        VARCHAR name UK
        VARCHAR agency
        DATE start_date
        DATE end_date
    }

    OBSERVATIONS {
        INT id PK
        INT telescope_id FK
        INT instrument_id FK
        INT mission_id FK
        VARCHAR target_type
        INT target_id
        DATETIME observed_at
        INT exposure_s
    }

    GALAXIES ||--o{ STAR_SYSTEMS : contains
    CONSTELLATIONS ||--o{ STAR_SYSTEMS : maps
    STAR_SYSTEMS ||--o{ STARS : has
    STARS ||--o{ PLANETS : has
    PLANETS ||--o{ MOONS : has
    TELESCOPES ||--o{ INSTRUMENTS : has
    TELESCOPES ||--o{ OBSERVATIONS : used_in
    INSTRUMENTS ||--o{ OBSERVATIONS : used_in
    MISSIONS ||--o{ OBSERVATIONS : context
```

## 3) Schemat dokumentowy - MongoDB

```mermaid
flowchart LR
    OBS[observations\n_id, telescope_id, instrument_id\nmission_id, target_type, target_id\nobserved_at, exposure_s]

    subgraph CORE[Domain collections]
        ST[stars\n_id, system_id, spectral_type]
        PL[planets\n_id, star_id, planet_type]
        SS[star_systems\n_id, galaxy_id, constellation_id]
        GA[galaxies\n_id, name, galaxy_type]
        CO[constellations\n_id, name, area_sq_deg]
        MO[moons\n_id, planet_id]
    end

    subgraph OBSCTX[Observation context]
        TE[telescopes\n_id, name, telescope_type]
        IN[instruments\n_id, telescope_id, wavelength_band]
        MI[missions\n_id, name, agency]
    end

    OBS -->|telescope_id| TE
    OBS -->|instrument_id| IN
    OBS -->|mission_id| MI
    OBS -->|target_id when target_type=star| ST
    OBS -->|target_id when target_type=planet| PL

    ST -->|system_id| SS
    PL -->|star_id| ST
    MO -->|planet_id| PL
    SS -->|galaxy_id| GA
    SS -->|constellation_id| CO
    IN -->|telescope_id| TE
```

Wzorzec dokumentu observations (przyklad):

{
\_id: Number,
telescope_id: Number,
instrument_id: Number,
mission_id: Number | null,
target_type: "star" | "planet",
target_id: Number,
observed_at: ISODate,
exposure_s: Number
}

## 4) Schemat dokumentowy - Neo4j (model grafowy)

```mermaid
flowchart LR
    G[Galaxy]
    C[Constellation]
    SS[StarSystem]
    S[Star]
    P[Planet]
    M[Moon]
    T[Telescope]
    I[Instrument]
    MS[Mission]
    O[Observation]

    G -->|HAS_SYSTEM| SS
    SS -->|IN_CONSTELLATION| C
    SS -->|HAS_STAR| S
    S -->|HAS_PLANET| P
    P -->|HAS_MOON| M

    T -->|HAS_INSTRUMENT| I

    O -->|USED_TELESCOPE| T
    O -->|USED_INSTRUMENT| I
    O -->|IN_MISSION| MS
    O -->|OBSERVED| S
    O -->|OBSERVED| P
```

Minimalny zestaw wlasciwosci:

- Galaxy: id, name, galaxy_type, distance_mly
- Constellation: id, name, area_sq_deg
- StarSystem: id, name, distance_ly
- Star: id, name, spectral_type, mass_solar, radius_solar
- Planet: id, name, planet_type, mass_earth, radius_earth, orbit_period_days
- Moon: id, name, mass_lunar, radius_lunar
- Telescope: id, name, telescope_type, location, aperture_m
- Instrument: id, name, wavelength_band, resolution_arcsec
- Mission: id, name, agency, start_date
- Observation: id, target_type, target_id, observed_at, exposure_s
