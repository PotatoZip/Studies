USE Airport;

SELECT plane_id, company
FROM plane
RIGHT JOIN  gate
on gate.gate_id = plane.plane_id;

SELECT parking_id, open_hours
FROM parking
RIGHT JOIN worker
on worker.working_hours = parking.open_hours;

SELECT plane_id, pasengers_slots
FROM plane
RIGHT JOIN parking
on parking.slots_count = plane.pasengers_slots;

SELECT runway_id, runway_number
FROM runway
LEFT JOIN gate
on runway.runway_number = gate.gate_number;

SELECT *
FROM shop
LEFT JOIN worker
on shop.open_hours > worker.working_hours;