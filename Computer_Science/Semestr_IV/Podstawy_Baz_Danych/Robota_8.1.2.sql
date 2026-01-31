create database airport5;
use airport5;

-- drop database airport5;

create table plane (
plane_id int(15) primary key,
company varchar(25),
weight int(15),
size int(15),
pasengers_slots int(15),
speed int(15));

create trigger ins_sum before insert on plane
for each row set @sum=@sum+new.weight;

create trigger ins_transaction before insert on plane
for each row precedes ins_sum
set @junk = @junk + if(new.weight>0, new.weight, 0),
@potentialPassengers = @potentialPassengers + if(new.pasengers_slots>0, new.pasengers_slots,0);

set @junk=0;
set @potentialPassengers=0;
insert into airport5.plane(plane_id, company, weight, size, pasengers_slots, speed)
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

select @junk as 'Total junk', @potentialPassengers as 'Total potential passengers'; 

set @sum=0;
insert into airport5.plane(plane_id, company, weight, size, pasengers_slots, speed) values ('91', 'EasyJet', '8000', '50', '102', '600');
select @sum as 'Total amount inserted';