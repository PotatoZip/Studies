create database company;
use company;
-- drop database company; 

create table employees(
id int auto_increment primary key,
job_id varchar(15) not null,
job_title varchar(45) not null,
min_salary int not null,
max_salary int not null
);

insert into company.employees(job_id, job_title, min_salary, max_salary)
values
('ad_press', 'President', 20000, 40000),
('ad_vp', 'Administration Vise President', 15000, 30000),
('ad_asst', 'Administration Assistant', 3000, 6000),
('fi_account', 'Accountant', 4200, 9000),
('ac_mgr', 'Acounting Manager', 8200, 16000),
('sa_mfn', 'Sales Manager', 10000, 20000),
('sa_rep', 'Sales Repesentative', 6000, 12000),
('st_clerk', 'Stok Clerk', 2000, 5000),
('it_prog', 'Programer', 4000, 10000),
('mk_man', 'Marketing Manager', 9000, 15000);

call my_proc_select2('Programer', @s);
