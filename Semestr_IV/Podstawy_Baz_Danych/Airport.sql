create database if not exists airport;
use airport;
-- drop database airport;
create table if not exists shop(
shop_id int(15) primary key,
product varchar(25),
shop_type varchar(25),
open_hours time);

create table if not exists cafe(
cafe_id int(15) primary key,
coffee_cost int(15),
tables_count int(15));


create table if not exists runway(
runway_id int(15) primary key,
runway_number int(15),
length int(25),
runway_condition char(15));

create table if not exists parking(
parking_id int(15) primary key,
slots_count int(15),
floor int(15),
open_hours time,
cost int(15));

create table if not exists plane(
plane_id int(15) primary key,
company varchar(25),
weight int(15),
size int(15),
pasengers_slots int(15),
speed int(15),
id_runway int(15),
foreign key (id_runway) references runway (runway_id) on update no action on delete no action);

create table if not exists gate(
gate_id int(15) primary key,
gate_number int(15),
id_plane int(15),
foreign key (id_plane) references plane (plane_id) on update no action on delete no action);

create table if not exists worker(
    worker_id int(15) primary key,
    worker_name varchar(25),
    age int(15),
    salary int(15),
    working_hours time,
    specialization varchar(25),
    id_shop int(15),
    id_cafe int(15),
    id_parking int(15),
    id_plane int(15),
    id_gate int(15),
    foreign key (id_shop) references shop (shop_id) on update no action on delete no action,
    foreign key (id_cafe) references cafe (cafe_id) on update no action on delete no action,
    foreign key (id_parking) references parking (parking_id) on update no action on delete no action,
    foreign key (id_plane) references plane (plane_id) on update no action on delete no action,
    foreign key (id_gate) references gate (gate_id) on update no action on delete no action);

insert into airport.shop(shop_id, product, shop_type, open_hours)
values 
('1', 'water', 'grossery', '09:30:00'),
('242', 'chocolate', 'grossery', '09:00:00'),
('553', 'beer', 'grossery', '09:00:00'),
('467', 'tea', 'tea shop', '07:00:00'),
('655', 'tedy bear', 'suvenire shop', '09:00:00'),
('69', 'flowers', 'florist', '08:00:00'),
('73', 'perfume', 'galantery', '09:00:00'),
('81', 'water', 'grossery', '09:00:00'),
('0899', 'water', 'grossery', '10:00:00'),
('170', 'water', 'grossery', '09:00:00');

insert into airport.cafe(cafe_id, coffee_cost, tables_count)
values 
('122', '20', '10'),
('254', '20', '75'),
('83', '30', '10'),
('475', '20', '10'),
('50', '20', '20'),
('6009', '20', '60'),
('798', '16', '10'),
('87', '10', '10'),
('978', '20', '9'),
('190', '20', '34');

insert into airport.plane(plane_id, company, weight, size, pasengers_slots, speed)
values 
('111', 'EasyJet', '1000', '50', '10', '500'),
('224', 'Ryaner', '1000', '50', '103', '500'),
('5253', 'Ryaner', '1000', '50', '200', '500'),
('4564', 'LOT', '1000', '50', '200', '500'),
('587', 'LOT', '1000', '50', '10', '600'),
('667', 'EasyJet', '1000', '50', '104', '550'),
('787', 'EasyJet', '1000', '50', '102', '550'),
('832', 'EasyJet', '1000', '50', '10', '550'),
('911', 'EasyJet', '1000', '50', '102', '600'),
('1110', 'Swishair', '1000', '50', '10', '750');

insert into airport.runway(runway_id, runway_number, length, runway_condition)
values 
('187', '1', '3000', 'A'),
('2998', '2', '3000', 'B'),
('3000', '3', '3000', 'A'),
('4989', '4', '3000', 'C'),
('54232', '5', '3000', 'A'),
('6289', '6', '10000', 'A'),
('762', '7', '3000', 'F'),
('853', '8', '3000', 'F'),
('9115', '9', '3000', 'A'),
('1650', '10', '200', 'A');

insert into airport.gate(gate_id, gate_number)
values 
('1112', '4'),
('2334', '4'),
('356', '5'),
('487', '5'),
('547', '3'),
('698', '3'),
('7098', '2'),
('8679', '2'),
('9447', '1'),
('1078', '1');

insert into airport.parking(parking_id, slots_count, floor, open_hours, cost)
values 
('781', '100', '3', '09:30:00', '45'),
('2985', '200', '2', '00:00:00', '45'),
('3478', '1000', '7', '00:00:00', '45'),
('4484', '100', '1', '00:00:00', '45'),
('5684', '100', '2', '08:00:00', '45'),
('647', '100', '4', '00:00:00', '45'),
('7654', '500', '1', '00:00:00', '45'),
('883', '230', '1', '10:00:00', '45'),
('9098', '40', '1', '17:30:00', '45'),
('1055', '100', '6', '00:00:00', '45');

insert into airport.worker(worker_id, worker_name, age, salary, working_hours, specialization)
values 
('173', 'Janek', '60', '3500', '09:00:00', 'worker'),
('25678', 'Pawel', '60', '3500', '09:00:00', 'worker'),
('353', 'Michał', '60', '3500', '09:00:00', 'worker'),
('4678', 'Piotr', '60', '3500', '09:00:00', 'worker'),
('563', 'Janek', '60', '3500', '09:00:00', 'worker'),
('628', 'Janek', '60', '3500', '09:00:00', 'worker'),
('757', 'Janek', '60', '3500', '09:00:00', 'worker'),
('82643', 'Janek', '60', '3500', '09:00:00', 'worker'),
('9578', 'Janek', '60', '3500', '09:00:00', 'worker'),
('1052', 'Janek', '60', '3500', '09:00:00', 'worker');

select * from airport.worker;
select * from airport.plane;