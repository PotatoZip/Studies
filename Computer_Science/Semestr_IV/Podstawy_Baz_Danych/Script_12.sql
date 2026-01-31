-- drop database airport4;
create database if not exists airport4;
use airport4;

create table if not exists runway(
runway_id int(15) primary key,
runway_number int(15),
length int(25),
runway_condition char(15));

create table if not exists plane(
plane_id int(15) primary key,
company varchar(25),
weight int(15),
size int(15),
pasengers_slots int(15),
speed int(15),
id_runway int(15));

insert into airport4.runway(runway_id, runway_number, length, runway_condition)
values 
('187', '1', '3000', 'A'),
('2998', '2', '3000', 'B'),
('3000', '3', '3000', 'A'),
('4989', '4', '5000', 'C'),
('54232', '5', '3000', 'A'),
('6289', '6', '10000', 'A'),
('762', '7', '3000', 'F'),
('853', '8', '4000', 'F'),
('9115', '9', '5000', 'A'),
('1650', '10', '200', 'A');

insert into airport4.plane(plane_id, company, weight, size, pasengers_slots, speed, id_runway)
values 
('111', 'EasyJet', '1000', '50', '10', '500', '187'),
('224', 'Ryaner', '1000', '50', '103', '500','2998'),
('5253', 'Ryaner', '2500', '50', '200', '500','3000'),
('4564', 'LOT', '1000', '50', '200', '500','4989'),
('1', 'LOT', '1000', '50', '10', '600','54232'),
('667', 'EasyJet', '3900', '50', '104', '550','6289'),
('787', 'EasyJet', '1000', '50', '102', '550','762'),
('832', 'EasyJet', '9000', '50', '10', '550','853'),
('911', 'EasyJet', '8000', '50', '102', '600','9115'),
('1110', 'Swishair', '200', '50', '10', '750','1650');

alter table runway add index runway_index(length);
explain select runway_id, runway_condition from runway
where length > 3000;

-- alter table runway add index runway_index(runway_condition, length);

-- select @avgSpeed := avg(speed) from plane;
-- select plane_id, size, speed from plane
-- where company in ('EasyJet', 'LOT') and speed > @avgSpeed;

explain select * from plane
where company in ('EasyJet', 'LOT') and speed > @avgSpeed;