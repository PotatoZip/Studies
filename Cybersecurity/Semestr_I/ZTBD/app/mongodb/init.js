db = db.getSiblingDB("astronomy");

// Kolekcja 1: Galaktyki
db.createCollection("galaxies");

// Dane inicjalne (seed data) – minimum potrzebne do uruchomienia
db.galaxies.insertMany([
  { _id: 1, name: "Milky Way", galaxy_type: "Spiral", distance_mly: 0.0 },
  { _id: 2, name: "Andromeda", galaxy_type: "Spiral", distance_mly: 2.54 },
]);

// Kolekcja 2: Konstelacje
// area_sq_deg – powierzchnia konstelacji w stopniach kwadratowych wg IAU
db.createCollection("constellations");
db.constellations.insertMany([
  { _id: 1, name: "Orion", area_sq_deg: 594.12 },
  { _id: 2, name: "Lyra", area_sq_deg: 286.48 },
]);

// Kolekcja 3: Systemy gwiezdne
// galaxy_id / constellation_id – referencje (równoważnik FK w SQL)
db.createCollection("star_systems");
db.star_systems.insertMany([
  {
    _id: 1,
    name: "Solar System",
    galaxy_id: 1,
    constellation_id: 1,
    distance_ly: 0.0,
  },
  {
    _id: 2,
    name: "Vega System",
    galaxy_id: 1,
    constellation_id: 2,
    distance_ly: 25.04,
  },
]);

// Kolekcja 4: Gwiazdy (referencja do star_systems przez system_id)
// spectral_type – klasyfikacja MK (np. G2V dla Słońca)
db.createCollection("stars");
db.stars.insertMany([
  {
    _id: 1,
    name: "Sun",
    system_id: 1,
    spectral_type: "G2V",
    mass_solar: 1.0,
    radius_solar: 1.0,
  },
  {
    _id: 2,
    name: "Vega",
    system_id: 2,
    spectral_type: "A0V",
    mass_solar: 2.135,
    radius_solar: 2.362,
  },
]);

// Kolekcja 5: Planety (referencja do stars przez star_id)
// planet_type – np. Terrestrial, Gas Giant, Ice Giant
// orbit_period_days – okres orbitalny w dniach ziemskich
db.createCollection("planets");
db.planets.insertMany([
  {
    _id: 1,
    name: "Earth",
    star_id: 1,
    planet_type: "Terrestrial",
    mass_earth: 1.0,
    radius_earth: 1.0,
    orbit_period_days: 365.25,
  },
  {
    _id: 2,
    name: "Mars",
    star_id: 1,
    planet_type: "Terrestrial",
    mass_earth: 0.107,
    radius_earth: 0.532,
    orbit_period_days: 687.0,
  },
  {
    _id: 3,
    name: "Vega b",
    star_id: 2,
    planet_type: "Gas Giant",
    mass_earth: 318.0,
    radius_earth: 11.2,
    orbit_period_days: 240.0,
  },
]);

// Kolekcja 6: Księżyce (referencja do planets przez planet_id)
// mass_lunar / radius_lunar – względem Księżyca Ziemskiego (1.0 = Księżyc)
db.createCollection("moons");
db.moons.insertMany([
  {
    _id: 1,
    name: "Moon",
    planet_id: 1,
    mass_lunar: 1.0,
    radius_lunar: 1.0,
    orbit_period_days: 27.3,
  },
  {
    _id: 2,
    name: "Phobos",
    planet_id: 2,
    mass_lunar: 0.000001,
    radius_lunar: 0.017,
    orbit_period_days: 0.32,
  },
]);

// Kolekcja 7: Teleskopy
// telescope_type – np. Space, Optical, Radio, Infrared
// aperture_m – średnica zwierciadła w metrach
db.createCollection("telescopes");
db.telescopes.insertMany([
  {
    _id: 1,
    name: "Hubble",
    telescope_type: "Space",
    location: "Low Earth Orbit",
    aperture_m: 2.4,
  },
  {
    _id: 2,
    name: "Keck I",
    telescope_type: "Optical",
    location: "Mauna Kea",
    aperture_m: 10.0,
  },
]);

// Kolekcja 8: Instrumenty naukowe (referencja do telescopes przez telescope_id)
// wavelength_band – zakres spektralny (UV-Vis, Optical, Infrared, Radio)
// resolution_arcsec – rozdzielczość kątowa w sekundach łukowych
db.createCollection("instruments");
db.instruments.insertMany([
  {
    _id: 1,
    name: "WFC3",
    telescope_id: 1,
    wavelength_band: "UV-Vis",
    resolution_arcsec: 0.04,
  },
  {
    _id: 2,
    name: "HIRES",
    telescope_id: 2,
    wavelength_band: "Optical",
    resolution_arcsec: 0.02,
  },
]);

// Kolekcja 9: Misje kosmiczne/obserwacyjne
// end_date – może być null gdy misja nadal aktywna
db.createCollection("missions");
db.missions.insertMany([
  {
    _id: 1,
    name: "Hubble Mission",
    agency: "NASA",
    start_date: new Date("1990-04-24"),
    end_date: null,
  },
  {
    _id: 2,
    name: "Keck Operations",
    agency: "W. M. Keck",
    start_date: new Date("1993-05-01"),
    end_date: null,
  },
]);

// Kolekcja 10: Obserwacje astronomiczne – kolekcja faktów (największa)
// Łączy telescope_id, instrument_id i mission_id przez referencje.
// target_type – 'star' lub 'planet' (polimorficzna referencja bez walidacji)
// target_id   – _id dokumentu z kolekcji stars lub planets
// exposure_s  – czas ekspozycji w sekundach
db.createCollection("observations");
db.observations.insertMany([
  {
    _id: 1,
    telescope_id: 1,
    instrument_id: 1,
    mission_id: 1,
    target_type: "star",
    target_id: 1,
    observed_at: new Date(),
    exposure_s: 1200,
  },
  {
    _id: 2,
    telescope_id: 2,
    instrument_id: 2,
    mission_id: 2,
    target_type: "planet",
    target_id: 1,
    observed_at: new Date(),
    exposure_s: 1800,
  },
]);
