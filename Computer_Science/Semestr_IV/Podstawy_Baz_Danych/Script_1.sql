USE Airport;

SELECT * FROM plane;

SELECT age, salary FROM worker;

SELECT pasengers_slots, plane_id FROM plane;

SELECT parking_id, slots_count FROM parking WHERE slots_count > 100;

SELECT cafe_id, tables_count FROM cafe WHERE tables_count < 20;