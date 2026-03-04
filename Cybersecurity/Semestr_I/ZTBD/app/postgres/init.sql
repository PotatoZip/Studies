-- Usunięcie tabel w kolejności odwrotnej do zależności FK
DROP TABLE IF EXISTS observations CASCADE;
DROP TABLE IF EXISTS instruments CASCADE;
DROP TABLE IF EXISTS missions CASCADE;
DROP TABLE IF EXISTS telescopes CASCADE;
DROP TABLE IF EXISTS moons CASCADE;
DROP TABLE IF EXISTS planets CASCADE;
DROP TABLE IF EXISTS stars CASCADE;
DROP TABLE IF EXISTS star_systems CASCADE;
DROP TABLE IF EXISTS constellations CASCADE;
DROP TABLE IF EXISTS galaxies CASCADE;

-- Tabela 1: Galaktyki
-- Przechowuje podstawowe informacje o galaktykach.
-- distance_mly – odległość w milionach lat świetlnych (0 = Droga Mleczna)
CREATE TABLE galaxies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    galaxy_type VARCHAR(40) NOT NULL,
    distance_mly NUMERIC(10, 2) NOT NULL
);

-- Tabela 2: Konstelacje
-- Obszary nieba wyznaczone przez IAU.
-- area_sq_deg – powierzchnia konstelacji w stopniach kwadratowych
CREATE TABLE constellations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    area_sq_deg NUMERIC(10, 2) NOT NULL
);

-- Tabela 3: Systemy gwiezdne
-- Grupy gwiazd powiązanych grawitacyjnie. FK do galaxies i constellations.
-- constellation_id może być NULL (system poza obszarem konstelacji)
-- distance_ly – odległość od Słońca w latach świetlnych
CREATE TABLE star_systems (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    galaxy_id INT NOT NULL REFERENCES galaxies(id),
    constellation_id INT REFERENCES constellations(id),
    distance_ly NUMERIC(12, 2) NOT NULL
);

-- Tabela 4: Gwiazdy
-- spectral_type – klasyfikacja MK (np. G2V dla Słońca, A0V dla Wegi)
-- mass_solar / radius_solar – masa i promień względem Słońca (1.0 = Słońce)
CREATE TABLE stars (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    system_id INT NOT NULL REFERENCES star_systems(id),
    spectral_type VARCHAR(10) NOT NULL,
    mass_solar NUMERIC(8, 3) NOT NULL,
    radius_solar NUMERIC(8, 3) NOT NULL
);

-- Tabela 5: Planety
-- planet_type – np. Terrestrial, Gas Giant, Ice Giant, Super-Earth
-- mass_earth / radius_earth – masa i promień względem Ziemi (1.0 = Ziemia)
-- orbit_period_days – okres orbitalny w dniach ziemskich
CREATE TABLE planets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    star_id INT NOT NULL REFERENCES stars(id),
    planet_type VARCHAR(30) NOT NULL,
    mass_earth NUMERIC(10, 3) NOT NULL,
    radius_earth NUMERIC(10, 3) NOT NULL,
    orbit_period_days NUMERIC(12, 2) NOT NULL
);

-- Tabela 6: Księżyce
-- mass_lunar / radius_lunar – masa i promień względem Księżyca Ziemskiego (1.0 = Księżyc)
-- orbit_period_days – okres obiegu wokół planety macierzystej
CREATE TABLE moons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    planet_id INT NOT NULL REFERENCES planets(id),
    mass_lunar NUMERIC(10, 3) NOT NULL,
    radius_lunar NUMERIC(10, 3) NOT NULL,
    orbit_period_days NUMERIC(12, 2) NOT NULL
);

-- Tabela 7: Teleskopy
-- telescope_type – np. Space, Optical, Radio, Infrared
-- aperture_m – średnica zwierciadła/obiektywu w metrach
CREATE TABLE telescopes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    telescope_type VARCHAR(40) NOT NULL,
    location VARCHAR(120) NOT NULL,
    aperture_m NUMERIC(6, 2) NOT NULL
);

-- Tabela 8: Instrumenty naukowe
-- Przypisane do konkretnego teleskopu (FK → telescopes).
-- wavelength_band – zakres spektralny (np. UV-Vis, Optical, Infrared, Radio)
-- resolution_arcsec – rozdzielczość kątowa w sekundach łukowych
CREATE TABLE instruments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    telescope_id INT NOT NULL REFERENCES telescopes(id),
    wavelength_band VARCHAR(40) NOT NULL,
    resolution_arcsec NUMERIC(8, 4) NOT NULL
);

-- Tabela 9: Misje kosmiczne/obserwacyjne
-- end_date może być NULL – misja nadal aktywna
CREATE TABLE missions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    agency VARCHAR(80) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE
);

-- Tabela 10: Obserwacje astronomiczne – tabela faktów (największa)
-- Łączy teleskop, instrument i misję w jednej obserwacji.
-- target_type – typ obiektu docelowego: 'star' lub 'planet'
-- target_id   – ID obiektu z tabeli stars lub planets (polimorficzna relacja)
-- exposure_s  – czas ekspozycji w sekundach
-- mission_id może być NULL (obserwacja poza zdefiniowaną misją)
CREATE TABLE observations (
    id SERIAL PRIMARY KEY,
    telescope_id INT NOT NULL REFERENCES telescopes(id),
    instrument_id INT NOT NULL REFERENCES instruments(id),
    mission_id INT REFERENCES missions(id),
    target_type VARCHAR(20) NOT NULL,
    target_id INT NOT NULL,
    observed_at TIMESTAMP NOT NULL,
    exposure_s INT NOT NULL
);

-- Dane inicjalne (seed data) – minimum potrzebne do uruchomienia

INSERT INTO galaxies (id, name, galaxy_type, distance_mly) VALUES
(1, 'Milky Way', 'Spiral', 0.00),
(2, 'Andromeda', 'Spiral', 2.54);

INSERT INTO constellations (id, name, area_sq_deg) VALUES
(1, 'Orion', 594.12),
(2, 'Lyra', 286.48);

INSERT INTO star_systems (id, name, galaxy_id, constellation_id, distance_ly) VALUES
(1, 'Solar System', 1, 1, 0.00),
(2, 'Vega System', 1, 2, 25.04);

INSERT INTO stars (id, name, system_id, spectral_type, mass_solar, radius_solar) VALUES
(1, 'Sun', 1, 'G2V', 1.000, 1.000),
(2, 'Vega', 2, 'A0V', 2.135, 2.362);

INSERT INTO planets (id, name, star_id, planet_type, mass_earth, radius_earth, orbit_period_days) VALUES
(1, 'Earth', 1, 'Terrestrial', 1.000, 1.000, 365.25),
(2, 'Mars', 1, 'Terrestrial', 0.107, 0.532, 687.00),
(3, 'Vega b', 2, 'Gas Giant', 318.000, 11.200, 240.00);

INSERT INTO moons (id, name, planet_id, mass_lunar, radius_lunar, orbit_period_days) VALUES
(1, 'Moon', 1, 1.000, 1.000, 27.32),
(2, 'Phobos', 2, 0.000001, 0.017, 0.32);

INSERT INTO telescopes (id, name, telescope_type, location, aperture_m) VALUES
(1, 'Hubble', 'Space', 'Low Earth Orbit', 2.40),
(2, 'Keck I', 'Optical', 'Mauna Kea', 10.00);

INSERT INTO instruments (id, name, telescope_id, wavelength_band, resolution_arcsec) VALUES
(1, 'WFC3', 1, 'UV-Vis', 0.04),
(2, 'HIRES', 2, 'Optical', 0.02);

INSERT INTO missions (id, name, agency, start_date, end_date) VALUES
(1, 'Hubble Mission', 'NASA', '1990-04-24', NULL),
(2, 'Keck Operations', 'W. M. Keck', '1993-05-01', NULL);

INSERT INTO observations (id, telescope_id, instrument_id, mission_id, target_type, target_id, observed_at, exposure_s) VALUES
(1, 1, 1, 1, 'star', 1, CURRENT_TIMESTAMP - INTERVAL '1 day', 1200),
(2, 2, 2, 2, 'planet', 1, CURRENT_TIMESTAMP - INTERVAL '2 days', 1800);