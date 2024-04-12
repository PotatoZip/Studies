USE Airport;

SELECT *
FROM cafe
ORDER BY coffee_cost DESC;

SELECT *
FROM parking
WHERE slots_count > 200
ORDER BY slots_count;

SELECT *
FROM worker
WHERE worker_name = 'Janek'
ORDER BY salary;

SELECT runway_id, length, runway_condition
FROM runway
WHERE length > 200
ORDER BY runway_condition;

SELECT *
FROM parking
WHERE floor > 2
ORDER BY floor;