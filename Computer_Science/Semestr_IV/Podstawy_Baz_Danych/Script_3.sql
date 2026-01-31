USE Airport;

SELECT *
FROM parking
WHERE floor BETWEEN 2 AND 6;

SELECT worker_id, salary
FROM worker
WHERE salary BETWEEN 5500 AND 100000;

SELECT plane_id, company
FROM plane
WHERE company in ('Swishair', 'Ryaner', 'LOT');

SELECT *
FROM cafe
WHERE coffee_cost LIKE 20;

SELECT *
FROM shop
WHERE open_hours LIKE '07:00:00';