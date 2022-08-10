ALTER TABLE teams AUTO_INCREMENT = 1;
SET @COUNT = 0;
UPDATE teams SET tid = @COUNT:=@COUNT+1;

DELETE FROM teams;

ALTER TABLE users AUTO_INCREMENT = 1;
SET @COUNT = 0;
UPDATE users SET uid = @COUNT:=@COUNT+1;

INSERT INTO teams (tid, tname, tadmin_uid, tlike, tview, tfounded) VALUES
	(0, 'qwer', 2, 0, 0, NOW());

INSERT INTO users (uid, id, pw, nickname, likes, playtime, avartar) VALUES
	(0, 'ioahsjdiof', 'vnasdofj', 'jkvnasiodjf', 0, 0, 0);

SELECT * FROM teams;

SELECT * FROM users;

SELECT * FROM companys