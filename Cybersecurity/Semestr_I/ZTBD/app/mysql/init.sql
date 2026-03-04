-- Usunięcie tabel w kolejności odwrotnej do zależności FK
DROP TABLE IF EXISTS observations;
DROP TABLE IF EXISTS instruments;
DROP TABLE IF EXISTS missions;
DROP TABLE IF EXISTS telescopes;
DROP TABLE IF EXISTS moons;
DROP TABLE IF EXISTS planets;
DROP TABLE IF EXISTS stars;
DROP TABLE IF EXISTS star_systems;
DROP TABLE IF EXISTS constellations;
DROP TABLE IF EXISTS galaxies;

-- Tabela 1: Galaktyki
-- distance_mly – odległość w milionach lat świetlnych (0 = Droga Mleczna)
CREATE TABLE galaxies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    galaxy_type VARCHAR(40) NOT NULL,
    distance_mly DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;

-- Tabela 2: Konstelacje
-- area_sq_deg – powierzchnia konstelacji w stopniach kwadratowych wg IAU
CREATE TABLE constellations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    area_sq_deg DECIMAL(10, 2) NOT NULL
) ENGINE=InnoDB;

-- Tabela 3: Systemy gwiezdne
-- constellation_id może być NULL (system poza obszarem konstelacji)
-- distance_ly – odległość od Słońca w latach świetlnych
CREATE TABLE star_systems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    galaxy_id INT NOT NULL,
    constellation_id INT,
    distance_ly DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (galaxy_id) REFERENCES galaxies(id),
    FOREIGN KEY (constellation_id) REFERENCES constellations(id)
) ENGINE=InnoDB;

-- Tabela 4: Gwiazdy
-- spectral_type – klasyfikacja MK (np. G2V dla Słońca)
-- mass_solar / radius_solar – względem Słońca (1.0 = Słońce)
CREATE TABLE stars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    system_id INT NOT NULL,
    spectral_type VARCHAR(10) NOT NULL,
    mass_solar DECIMAL(8, 3) NOT NULL,
    radius_solar DECIMAL(8, 3) NOT NULL,
    FOREIGN KEY (system_id) REFERENCES star_systems(id)
) ENGINE=InnoDB;

-- Tabela 5: Planety
-- planet_type – np. Terrestrial, Gas Giant, Ice Giant, Super-Earth
-- mass_earth / radius_earth – względem Ziemi (1.0 = Ziemia)
-- orbit_period_days – okres orbitalny w dniach ziemskich
CREATE TABLE planets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    star_id INT NOT NULL,
    planet_type VARCHAR(30) NOT NULL,
    mass_earth DECIMAL(10, 3) NOT NULL,
    radius_earth DECIMAL(10, 3) NOT NULL,
    orbit_period_days DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (star_id) REFERENCES stars(id)
) ENGINE=InnoDB;

-- Tabela 6: Księżyce
-- mass_lunar / radius_lunar – względem Księżyca Ziemskiego (1.0 = Księżyc)
CREATE TABLE moons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    planet_id INT NOT NULL,
    mass_lunar DECIMAL(10, 3) NOT NULL,
    radius_lunar DECIMAL(10, 3) NOT NULL,
    orbit_period_days DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (planet_id) REFERENCES planets(id)
) ENGINE=InnoDB;

-- Tabela 7: Teleskopy
-- telescope_type – np. Space, Optical, Radio, Infrared
-- aperture_m – średnica zwierciadła w metrach
CREATE TABLE telescopes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    telescope_type VARCHAR(40) NOT NULL,
    location VARCHAR(120) NOT NULL,
    aperture_m DECIMAL(6, 2) NOT NULL
) ENGINE=InnoDB;

-- Tabela 8: Instrumenty naukowe (przypisane do teleskopu)
-- wavelength_band – zakres spektralny (UV-Vis, Optical, Infrared, Radio)
-- resolution_arcsec – rozdzielczość kątowa w sekundach łukowych
CREATE TABLE instruments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    telescope_id INT NOT NULL,
    wavelength_band VARCHAR(40) NOT NULL,
    resolution_arcsec DECIMAL(8, 4) NOT NULL,
    FOREIGN KEY (telescope_id) REFERENCES telescopes(id)
) ENGINE=InnoDB;

-- Tabela 9: Misje kosmiczne/obserwacyjne
-- end_date może być NULL – misja nadal aktywna
CREATE TABLE missions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) UNIQUE NOT NULL,
    agency VARCHAR(80) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE
) ENGINE=InnoDB;

-- Tabela 10: Obserwacje astronomiczne – tabela faktów (największa)
-- Łączy teleskop, instrument i misję w jednym rekordzie obserwacji.
-- target_type – 'star' lub 'planet' (polimorficzna relacja bez FK)
-- target_id   – ID z tabeli stars lub planets
-- exposure_s  – czas ekspozycji w sekundach
-- mission_id może być NULL (obserwacja poza zdefiniowaną misją)
CREATE TABLE observations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telescope_id INT NOT NULL,
    instrument_id INT NOT NULL,
    mission_id INT,
    target_type VARCHAR(20) NOT NULL,
    target_id INT NOT NULL,
    observed_at DATETIME NOT NULL,
    exposure_s INT NOT NULL,
    FOREIGN KEY (telescope_id) REFERENCES telescopes(id),
    FOREIGN KEY (instrument_id) REFERENCES instruments(id),
    FOREIGN KEY (mission_id) REFERENCES missions(id)
) ENGINE=InnoDB;

-- Dane inicjalne do tabel – tylko kilka rekordów dla celów testowych i demonstracyjnych.

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
(1, 1, 1, 1, 'star', 1, DATE_SUB(NOW(), INTERVAL 1 DAY), 1200),
(2, 2, 2, 2, 'planet', 1, DATE_SUB(NOW(), INTERVAL 2 DAY), 1800);