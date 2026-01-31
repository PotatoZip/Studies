USE Airport;

DROP VIEW IF EXISTS RichWorkers;
CREATE VIEW RichWorkers AS
SELECT salary, worker_name
FROM worker
WHERE salary > 10000;

SELECT * FROM RichWorkers;

DROP VIEW IF EXISTS BadRunways;
CREATE VIEW BadRunways AS
SELECT *
FROM runway
WHERE runway_condition = 'C';

SELECT * FROM BadRunways;