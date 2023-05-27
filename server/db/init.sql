
DROP EVENT IF EXISTS DELETE_OLD_SESSIONS;

DROP TABLE IF EXISTS GAME_STATISTIC;
DROP TABLE IF EXISTS USERS_SESSIONS;
DROP TABLE IF EXISTS USERS;

CREATE TABLE USERS (

    ID INT AUTO_INCREMENT PRIMARY KEY,
    REGISTRATION_STATE VARCHAR(64),
    NAME VARCHAR(64) NOT NULL,
    SURNAME VARCHAR(64) NOT NULL,
    EMAIL VARCHAR(64) NOT NULL,
    PW VARCHAR(64) NOT NULL,
    DEGREE VARCHAR(64) NOT NULL

);

CREATE TABLE GAME_STATISTIC (

    ID INT AUTO_INCREMENT PRIMARY KEY,
    ID_USER INT NOT NULL,
    POINTS INT NOT NULL,

    CONSTRAINT FOREIGN KEY (ID_USER) REFERENCES USERS(ID)
);

CREATE TABLE USERS_SESSIONS (
        USER_TOKEN VARCHAR(64) PRIMARY KEY,
        ID_USER INT NOT NULL,
        CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT FOREIGN KEY (ID_USER) REFERENCES USERS(ID)
    );

CREATE EVENT DELETE_OLD_SESSIONS
	ON SCHEDULE EVERY 1 DAY STARTS (
	    TIMESTAMP(CURRENT_DATE) + INTERVAL 1 DAY + INTERVAL 1 HOUR
	)
	DO DELETE FROM USERS_SESSIONS WHERE
    CREATED_AT < DATE_SUB(NOW(), INTERVAL 30 DAY);
