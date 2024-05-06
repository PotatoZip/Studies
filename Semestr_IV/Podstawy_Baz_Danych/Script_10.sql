create database if not exists airport3;
use airport3;
-- drop database airport3;
SET GLOBAL event_scheduler = ON;

create table if not exists parking3(
parking_id int primary key auto_increment,
hello_message varchar(15),
created_at datetime);

-- zdarzenie jednorazowe usuwane po wykonaniu
CREATE EVENT IF NOT EXISTS test_event_1
	ON SCHEDULE AT CURRENT_TIMESTAMP
	DO
		INSERT INTO parking3(hello_message, created_at)
		VALUES('Jednorazowe przywitanie', NOW());
        
-- zdarzenie jednorazowe nie usuwane po wykonaniu
CREATE EVENT IF NOT EXISTS test_event_2
	ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL 1 MINUTE
    ON COMPLETION PRESERVE
	DO
		INSERT INTO parking3(hello_message, created_at)
		VALUES('Stale przywitanie', NOW());
        
-- zdarzenie cykliczne
CREATE EVENT IF NOT EXISTS test_event_3
	ON SCHEDULE EVERY 30 SECOND
    STARTS CURRENT_TIMESTAMP
    ENDS CURRENT_TIMESTAMP + INTERVAL 1 HOUR
	DO
		INSERT INTO parking3(hello_message, created_at)
		VALUES('Witamy cie na okraglo', NOW());
        
SELECT * FROM parking3;

SHOW EVENTS FROM airport3;