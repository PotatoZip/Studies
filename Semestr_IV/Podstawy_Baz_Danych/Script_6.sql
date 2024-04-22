USE Airport;

SELECT SUM(coffee_cost) as total_cost FROM cafe;
SELECT SUM(cost) as total_cost FROM parking;
SELECT MIN(age) as youngest FROM worker;

SELECT
	CASE
		WHEN coffee_cost > 20 THEN 'Expensive'
        ELSE 'Affordable'
	END AS if_expensive
FROM cafe;

SELECT
	CASE
		WHEN runway_condition = 'A' THEN 'Good'
        ELSE 'BAD'
	END AS if_condition
FROM runway;
