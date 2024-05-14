create schema tryger_demo;
use tryger_demo;

-- drop schema tryger_demo;

create table account (act_num int, amount decimal(10,2));

create table test1(a1 int);
create table test2(a2 int);
create table test3(a3 int not null auto_increment primary key);
create table test4(
a4 int not null auto_increment primary key,
b4 int default 0
);

delimiter |
create trigger testref before insert on test1
	for each row
    begin
		insert into test2 set a2 = new.a1;
        delete from test3 where a3 = new.a1;
        update test4 set b4 = b4 + 1 where a4 = new.a1;
	end;
|
delimiter ;

create trigger ins_sum before insert on account
for each row set @sum=@sum+new.amount;

create trigger ins_transaction before insert on account
for each row precedes ins_sum
set @deposits = @deposits + if(new.amount>0, new.amount, 0),
@withdrawals = @withdrawals + if(new.amount<0, -new.amount,0);

delimiter //
create trigger upd_check before update on account
	for each row
	begin
		if new.amount < 0 then
			set new.amount = 0;
		elseif new.amount > 100 then
			set new.amount = 100;
		end if;
	end;//

set @deposits=0;
set @withdrawals=0;
insert into account values (137, 14.98), (141, 1937.50), (97, -100.00);
insert into account values (1324, 134.98), (41, 1937.50), (97, -100.00);
insert into account values (12, 14.985), (1641, 1937.50), (7, -100.00);

insert into test3 (a3) values
	(null), (null), (null), (null), (null),
    (null), (null), (null), (null), (null);
    
insert into test4 (a4) values
	(0), (0), (0), (0), (0), (0), (0), (0), (0), (0);
    
insert into test1 values
	(1), (3), (1), (7), (1), (8), (4), (4);
    
select * from test1, test2, test3 ,test4;

update account set amount = -10 where act_num = 97;
update account set amount = -20 where act_num = 7;
select * from account;
select @deposits as 'Total deposits', @withdrawals as 'Total withdrawls'; 

set @sum=0;
insert into account values (137, 14.98), (141, 1937.50), (97, -100.00);
select @sum as 'Total amount inserted';