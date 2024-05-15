create schema railway;
use railway;

create table train (
id int primary key, 
start_station varchar(20) not null,
finish_station varchar(20) not null
);

create table account_bank (
account_number int not null primary key,
balans int
);

insert into account_bank
values
('12345678', 5000),
('42345255', 15000),
('46222774', 7000),
('83242746', 3400),
('76234213', 1000);

start transaction;
update account_bank set balans=balans-2500 where account_number = 46222774;
update account_bank set balans=balans+2500 where account_number = 83242746;
select * from account_bank;
rollback;
select * from account_bank;
update account_bank set balans=balans-2500 where account_number = 46222774;
update account_bank set balans=balans+2500 where account_number = 83242746;
select * from account_bank;
commit;
select * from account_bank;

/*
start transaction;
insert into train values(760, 'Lwiw', 'Kowel');
select * from train where start_station = 'Lviv';
rollback;
select * from train where start_station = 'Lviv';
insert into train values(760, 'Lviv', 'Kovel');
commit;
select * from train where start_station = 'Lviv';
*/