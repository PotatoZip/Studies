create database if not exists airport;
use airport;

create table if not exists shop(
shop_id int(15) primary key,
product varchar(25),
shop_type varchar(25),
open_hours time);

create table if not exists cafe(
cafe_id int(15) primary key,
coffee_cost int(15),
tables_count int(15));

create table if not exists worker(
    worker_id int(15) primary key,
    worker_name varchar(25),
    age int(15),
    salary int(15),
    working_hours time,
    specialization varchar(25),
    id_shop int(15),
    id_cafe int(15),
    foreign key (id_shop) references shop (shop_id) on update no action on delete no action,
    foreign key (id_cafe) references cafe (cafe_id) on update no action on delete no action,
    parking_id int(15),
    plane_id int(15),
    gate_id int(15));

create table if not exists plane(
plane_id int(15) primary key,
company varchar(25),
weight int(15),
size int(15),
pasengers_slots int(15),
speed int(15),
runway_id int(15));

create table if not exists runway(
runway_id int(15) primary key,
runway_number int(15),
length int(25),
runway_condition char(15));

create table if not exists gate(
gate_id int(15) primary key,
gate_number int(15),
plane_id int(15));

create table if not exists parking(
parking_id int(15) primary key,
slots_count int(15),
floor int(15),
open_hours time,
cost int(15));

insert into airport.shop(shop_id, product, shop_type, open_hours)
values ('1', 'water', 'grossery', '09:00:00'),
('2', 'water', 'grossery', '09:00:00'),
('3', 'water', 'grossery', '09:00:00'),
('4', 'water', 'grossery', '09:00:00'),
('5', 'water', 'grossery', '09:00:00'),
('6', 'water', 'grossery', '09:00:00'),
('7', 'water', 'grossery', '09:00:00'),
('8', 'water', 'grossery', '09:00:00'),
('9', 'water', 'grossery', '09:00:00'),
('10', 'water', 'grossery', '09:00:00');

insert into airport.cafe(cafe_id, coffe_cost, tables_count)
values ('1', 'water', 'grossery'),
('2', 'water', 'grossery'),
('3', 'water', 'grossery'),
('4', 'water', 'grossery'),
('5', 'water', 'grossery'),
('6', 'water', 'grossery'),
('7', 'water', 'grossery'),
('8', 'water', 'grossery'),
('9', 'water', 'grossery'),
('10', 'water', 'grossery');

insert into airport.plane(plane_id, company, weight, size, pasengers_slots, speed)
values ('1', 'water', 'grossery'),
('2', 'water', 'grossery'),
('3', 'water', 'grossery'),
('4', 'water', 'grossery'),
('5', 'water', 'grossery'),
('6', 'water', 'grossery'),
('7', 'water', 'grossery'),
('8', 'water', 'grossery'),
('9', 'water', 'grossery'),
('10', 'water', 'grossery');

select * from airport.shop;