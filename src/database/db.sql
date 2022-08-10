DROP DATABASE IF EXISTS test;
CREATE DATABASE test;
--	DEFAULT CHARACTER SET utf8mb4
--	DEFAULT COLLATE utf8mb4_general_ci;
-- 왜 적으면 안됨?
-- 미친놈인가?

USE test;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
	`id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	`pw` VARCHAR(10) NOT NULL
) ENGINE=InnoDB;
--	CHARACTER SET utf8mb4
--	COLLATE utf8mb4_general_ci;

INSERT INTO users VALUES
	(null, 'qwer1234'),
	(null, 'asdf1234');