CREATE TABLE news (
            ID         INT IDENTITY(1,1) PRIMARY KEY,
            NAME       varchar(5000) NOT NULL,
            DATE       date,
            LINK       varchar(5000) NOT NULL
);

SELECT * FROM NEWS; 
--INSERT INTO news (NAME, DATE, LINK) VALUES ('Igor', '2023-04-09', 'value2');