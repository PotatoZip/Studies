create database airport7;
use airport7;
-- drop database airport7;

create table plane (
plane_id int(15) primary key,
company varchar(25),
weight int(15),
size int(15),
pasengers_slots int(15),
speed int(15));

insert into airport7.plane(plane_id, company, weight, size, pasengers_slots, speed)
values 
('111', 'EasyJet', '1000', '50', '10', '500'),
('224', 'Ryaner', '1000', '50', '103', '500'),
('5253', 'Ryaner', '2500', '50', '200', '500'),
('4564', 'LOT', '1000', '50', '200', '500'),
('1', 'LOT', '1000', '50', '10', '600'),
('667', 'EasyJet', '3900', '50', '104', '550'),
('787', 'EasyJet', '1000', '50', '102', '550'),
('832', 'EasyJet', '9000', '50', '10', '550'),
('911', 'EasyJet', '8000', '50', '102', '600'),
('1110', 'Swishair', '200', '50', '10', '750');

call search_plane(787);