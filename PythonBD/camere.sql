CREATE DATABASE hotel;

USE hotel;

CREATE TABLE camere (
    IdCamera INT AUTO_INCREMENT PRIMARY KEY,
    NrCamera INT NOT NULL,
    Etaj INT,
    Pret DECIMAL(10, 2)
);

INSERT INTO camere (NrCamera, Etaj, Pret) VALUES
(101, 1, 100.00),
(102, 1, 150.00),
(201, 2, 200.00),
(202, 2, 250.00),
(301, 3, 300.00),
(302, 3, 350.00);

SELECT * FROM camere;
