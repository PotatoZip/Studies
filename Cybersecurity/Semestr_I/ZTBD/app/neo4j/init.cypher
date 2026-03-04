// Węzeł 1: Galaxy – galaktyki
// distance_mly – odległość w milionach lat świetlnych (0 = Droga Mleczna)
CREATE (g1:Galaxy {id: 1, name: 'Milky Way', galaxy_type: 'Spiral', distance_mly: 0.0})
CREATE (g2:Galaxy {id: 2, name: 'Andromeda', galaxy_type: 'Spiral', distance_mly: 2.54})

// Węzeł 2: Constellation – konstelacje wg klasyfikacji IAU
CREATE (c1:Constellation {id: 1, name: 'Orion', area_sq_deg: 594.12})
CREATE (c2:Constellation {id: 2, name: 'Lyra', area_sq_deg: 286.48})

// Węzeł 3: StarSystem – systemy gwiezdne
// galaxy_id / constellation_id przechowywane jako właściwości do łączenia relacji
CREATE (s1:StarSystem {id: 1, name: 'Solar System', distance_ly: 0.0})
CREATE (s2:StarSystem {id: 2, name: 'Vega System', distance_ly: 25.04})

// Węzeł 4: Star – gwiazdy
// spectral_type – klasyfikacja MK (np. G2V dla Słońca, A0V dla Wegi)
// mass_solar / radius_solar – względem Słońca (1.0 = Słońce)
CREATE (st1:Star {id: 1, name: 'Sun', spectral_type: 'G2V', mass_solar: 1.0, radius_solar: 1.0})
CREATE (st2:Star {id: 2, name: 'Vega', spectral_type: 'A0V', mass_solar: 2.135, radius_solar: 2.362})

// Węzeł 5: Planet – planety
// planet_type – np. Terrestrial, Gas Giant, Ice Giant
// mass_earth / radius_earth – względem Ziemi (1.0 = Ziemia)
// orbit_period_days – okres orbitalny w dniach ziemskich
CREATE (p1:Planet {id: 1, name: 'Earth', planet_type: 'Terrestrial', mass_earth: 1.0, radius_earth: 1.0, orbit_period_days: 365.25})
CREATE (p2:Planet {id: 2, name: 'Mars', planet_type: 'Terrestrial', mass_earth: 0.107, radius_earth: 0.532, orbit_period_days: 687.0})
CREATE (p3:Planet {id: 3, name: 'Vega b', planet_type: 'Gas Giant', mass_earth: 318.0, radius_earth: 11.2, orbit_period_days: 240.0})

// Węzeł 6: Moon – księżyce
// mass_lunar / radius_lunar – względem Księżyca Ziemskiego (1.0 = Księżyc)
CREATE (m1:Moon {id: 1, name: 'Moon', mass_lunar: 1.0, radius_lunar: 1.0})
CREATE (m2:Moon {id: 2, name: 'Phobos', mass_lunar: 0.000001, radius_lunar: 0.017})

// Węzeł 7: Telescope – teleskopy
// telescope_type – np. Space, Optical, Radio, Infrared
// aperture_m – średnica zwierciadła w metrach
CREATE (t1:Telescope {id: 1, name: 'Hubble', telescope_type: 'Space', location: 'Low Earth Orbit', aperture_m: 2.4})
CREATE (t2:Telescope {id: 2, name: 'Keck I', telescope_type: 'Optical', location: 'Mauna Kea', aperture_m: 10.0})

// Węzeł 8: Instrument – instrumenty naukowe teleskopu
// wavelength_band – zakres spektralny (UV-Vis, Optical, Infrared, Radio)
// resolution_arcsec – rozdzielczość kątowa w sekundach łukowych
CREATE (i1:Instrument {id: 1, name: 'WFC3', wavelength_band: 'UV-Vis', resolution_arcsec: 0.04})
CREATE (i2:Instrument {id: 2, name: 'HIRES', wavelength_band: 'Optical', resolution_arcsec: 0.02})

// Węzeł 9: Mission – misje kosmiczne/obserwacyjne
CREATE (ms1:Mission {id: 1, name: 'Hubble Mission', agency: 'NASA', start_date: date('1990-04-24')})
CREATE (ms2:Mission {id: 2, name: 'Keck Operations', agency: 'W. M. Keck', start_date: date('1993-05-01')})

// Węzeł 10: Observation – obserwacje astronomiczne (węzły faktów, najliczniejsze)
// target_type – 'star' lub 'planet' (polimorficzna relacja OBSERVED)
// target_id   – id węzła Star lub Planet
// exposure_s  – czas ekspozycji w sekundach
CREATE (o1:Observation {id: 1, target_type: 'star', target_id: 1, observed_at: datetime(), exposure_s: 1200})
CREATE (o2:Observation {id: 2, target_type: 'planet', target_id: 1, observed_at: datetime(), exposure_s: 1800})

// Relacje między węzłami
WITH g1, g2, c1, c2, s1, s2, st1, st2, p1, p2, p3, m1, m2, t1, t2, i1, i2, ms1, ms2, o1, o2

// Galaktyki → Systemy gwiezdne
CREATE (g1)-[:HAS_SYSTEM]->(s1)
CREATE (g1)-[:HAS_SYSTEM]->(s2)

// Systemy gwiezdne → Konstelacje
CREATE (s1)-[:IN_CONSTELLATION]->(c1)
CREATE (s2)-[:IN_CONSTELLATION]->(c2)

// Systemy gwiezdne → Gwiazdy
CREATE (s1)-[:HAS_STAR]->(st1)
CREATE (s2)-[:HAS_STAR]->(st2)

// Gwiazdy → Planety
CREATE (st1)-[:HAS_PLANET]->(p1)
CREATE (st1)-[:HAS_PLANET]->(p2)
CREATE (st2)-[:HAS_PLANET]->(p3)

// Planety → Księżyce
CREATE (p1)-[:HAS_MOON]->(m1)
CREATE (p2)-[:HAS_MOON]->(m2)

// Teleskopy → Instrumenty
CREATE (t1)-[:HAS_INSTRUMENT]->(i1)
CREATE (t2)-[:HAS_INSTRUMENT]->(i2)

// Obserwacje → Instrumenty / Teleskopy / Misje / Obiekty docelowe
CREATE (o1)-[:USED_INSTRUMENT]->(i1)
CREATE (o2)-[:USED_INSTRUMENT]->(i2)
CREATE (o1)-[:USED_TELESCOPE]->(t1)
CREATE (o2)-[:USED_TELESCOPE]->(t2)
CREATE (o1)-[:IN_MISSION]->(ms1)
CREATE (o2)-[:IN_MISSION]->(ms2)
CREATE (o1)-[:OBSERVED]->(st1)
CREATE (o2)-[:OBSERVED]->(p1);
