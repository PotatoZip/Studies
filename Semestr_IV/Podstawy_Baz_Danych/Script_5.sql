USE Airport;

SELECT plane.company, runway.runway_condition
FROM plane
INNER JOIN runway
ON plane.id_runway = runway.runway_id;

SELECT parking.open_hours, worker.working_hours
FROM parking
RIGHT JOIN worker
on worker.id_parking = parking.parking_id;

SELECT gate.gate_number, plane.company
FROM gate
RIGHT JOIN plane
on gate.id_plane = plane.plane_id;

SELECT worker.salary, gate.gate_number
FROM worker
LEFT JOIN gate
on worker.id_gate = gate.gate_id;

SELECT shop.product, worker.salary
FROM shop
RIGHT JOIN worker
on worker.id_shop = shop.shop_id;