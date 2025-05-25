
CREATE TABLE system1 (
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP PRIMARY KEY,
    temperature DECIMAL(4,1),
    motorOverride BOOLEAN,
    controlled BOOLEAN,
    startTemp INT
);

CREATE TABLE system2 (
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP PRIMARY KEY,
    soilMoisture DECIMAL(5,2),
    temperature DECIMAL(4,1),
    humidity DECIMAL(4,1),
    moistureValue INT
);

CREATE TABLE system3 (
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP PRIMARY KEY,
    potentiometer FLOAT,
    button BOOLEAN,
    motionSensor BOOLEAN
);

