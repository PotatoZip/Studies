USE Airport;

SELECT *
FROM cafe
GROUP BY cafe_id
HAVING coffee_cost > 10;

SELECT *
FROM gate
HAVING gate_number < 3;

SELECT *
FROM runway
HAVING length > 200 AND length < 10000;

SELECT parking_id, floor
FROM parking
HAVING floor = 1;

SELECT worker_id, worker_name, age
FROM worker
GROUP BY worker_id
HAVING age > 30;