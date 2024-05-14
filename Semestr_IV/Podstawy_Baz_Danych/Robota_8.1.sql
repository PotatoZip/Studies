create schema tryger_demo;
use tryger_demo;

-- drop schema tryger_demo;

create table account (act_num int, amount decimal(10,2));

create trigger ins_sum before insert on account
for each row set @sum=@sum+new.amount;

create trigger ins_transaction before insert on account
for each row precedes ins_sum
set @deposits = @deposits + if(new.amount>0, new.amount, 0),
@withdrawals = @withdrawals + if(new.amount<0, -new.amount,0);

set @deposits=0;
set @withdrawals=0;
insert into account values (137, 14.98), (141, 1937.50), (97, -100.00);
insert into account values (1324, 134.98), (41, 1937.50), (9, -100.00);
insert into account values (12, 14.985), (1641, 1937.50), (7, -100.00);
select @deposits as 'Total deposits', @withdrawals as 'Total withdrawls'; 

set @sum=0;
insert into account values (137, 14.98), (141, 1937.50), (97, -100.00);
select @sum as 'Total amount inserted';