USE Airport;

SELECT company
FROM plane
UNION
SELECT product
FROM shop;

SELECT pasengers_slots
FROM plane
UNION
SELECT slots_count
FROM parking;

SELECT coffee_cost
FROM cafe
INTERSECT
SELECT cost
FROM parking;

SELECT open_hours
FROM parking
INTERSECT
SELECT working_hours
FROM worker;

SELECT floor
FROM parking
EXCEPT
SELECT gate_number
FROM gate;