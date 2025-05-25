CREATE DATABASE air_conditioning_system;
USE air_conditioning_system;
CREATE TABLE temperature_readings(id INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL, temperature DECIMAL(4,1));
CREATE TABLE motor_control(id INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL, motorOverrride boolean, controlled boolean, startTemp INT(11));
INSERT INTO motor_control (motorOverrride,controlled,startTemp) VALUES (0,0,25);