create database if not exists airport2;
use airport2;
--  drop database airport2;
create table if not exists parking2(
parking_id int(15) primary key,
slots_count int(15),
floor int(15),
open_hours time,
cost int(15));

create table if not exists worker2(
    worker_id int(15) primary key,
    worker_name varchar(25),
    age int(15),
    salary int(15),
    working_hours time,
    specialization varchar(25));

insert into airport2.worker2(worker_id, worker_name, age, salary, working_hours, specialization)
values 
('73', 'Janek', '60', '3500', '09:00:00', 'worker'),
('5678', 'Pawel', '60', '3500', '00:00:00', 'worker'),
('353', 'Michał', '35', '34500', '00:00:00', 'worker'),
('4678', 'Piotr', '25', '3500', '09:00:00', 'worker'),
('563', 'Janek', '60', '3500', '09:00:00', 'worker'),
('628', 'Janek', '25', '3500', '09:00:00', 'worker'),
('757', 'Janek', '35', '3500', '09:30:00', 'worker'),
('82643', 'Janek', '25', '2500', '09:00:00', 'worker'),
('9578', 'Janek', '25', '3500', '09:00:00', 'worker'),
('1052', 'Janek', '11', '53500', '09:00:00', 'worker');

insert into airport2.parking2(parking_id, slots_count, floor, open_hours, cost)
values 
('71', '100', '3', '09:30:00', '45'),
('2985', '200', '2', '00:00:00', '45'),
('3478', '1000', '7', '00:00:00', '45'),
('4484', '100', '1', '00:00:00', '45'),
('5684', '20', '2', '08:00:00', '45'),
('647', '20', '4', '00:00:00', '45'),
('7654', '500', '1', '00:00:00', '45'),
('883', '230', '1', '10:00:00', '45'),
('9098', '40', '1', '17:30:00', '45'),
('1055', '100', '6', '00:00:00', '45');

-- RANG
ALTER TABLE worker2
PARTITION BY RANGE (worker_id) (
	PARTITION p0 VALUES LESS THAN (200),
    PARTITION p1 VALUES LESS THAN (400),
    PARTITION p2 VALUES LESS THAN (MAXVALUE)
);

ALTER TABLE parking2
PARTITION BY RANGE (parking_id) (
	PARTITION p0 VALUES LESS THAN (200),
    PARTITION p1 VALUES LESS THAN (400),
    PARTITION p2 VALUES LESS THAN (MAXVALUE)
);

-- LIST
ALTER TABLE worker2
PARTITION BY LIST (worker_id) (
	PARTITION p0 VALUES IN (1, 2),
    PARTITION p1 VALUES IN (3, 4),
    PARTITION p2 VALUES IN (5, 6)
);

ALTER TABLE parking2
PARTITION BY LIST (parking_id) (
	PARTITION p0 VALUES IN (1, 2),
    PARTITION p1 VALUES IN (3, 4),
    PARTITION p2 VALUES IN (5, 6)
);

-- HASH
ALTER TABLE worker2
PARTITION BY HASH (worker_id) PARTITIONS 4;

ALTER TABLE parking2
PARTITION BY RANGE (parking_id) PARTITIONS 4;

SELECT * FROM worker2 PARTITION(p0);
SELECT * FROM parking2 PARTITION(p2);