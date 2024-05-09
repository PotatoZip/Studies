create schema productdb;
use productdb;
-- drop schema productdb; 

create table product(
id int auto_increment primary key,
product_name varchar(30) not null,
manufacturer varchar(30) not null,
product_count int default 0,
price decimal not null
);

insert into product(product_name, manufacturer, product_count, price)
values
('iphone X', 'Apple', 2, 7600),
('iphone 8', 'Apple', 2, 5600),
('iphone 7', 'Apple', 4, 4600),
('iphone 6', 'Apple', 2, 3600),
('Nokia 3444', 'Nokia', 6, 2600),
('Nokia 3333', 'Nokia', 6, 1600),
('Nokia 3310', 'Nokia', 4, 1100);

alter table product add index manufact_price(manufacturer, price);
explain select * from product where manufacturer='Nokia' and price < 2000;