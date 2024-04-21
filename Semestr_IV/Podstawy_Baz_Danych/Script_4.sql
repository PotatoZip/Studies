USE Airport;

SELECT tables_count, coffee_cost
FROM cafe
GROUP BY tables_count, coffee_cost
HAVING coffee_cost > 10;

SELECT id_plane, gate_number
FROM gate
GROUP BY id_plane, gate_number
HAVING gate_number < 3;

SELECT runway_number, length
FROM runway
GROUP BY runway_number, length
HAVING length > 200 AND length < 10000;


SELECT parking_id, floor
FROM parking
GROUP BY parking_id, floor
HAVING floor = 1;

SELECT worker_name, age
FROM worker
GROUP BY worker_name, age
HAVING age > 30;