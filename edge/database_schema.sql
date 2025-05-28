
CREATE TABLE system1 (
    timestamp DATETIME(3) DEFAULT CURRENT_TIMESTAMP(3) PRIMARY KEY,
    temperature DECIMAL(4,1),
    motorOverride BOOLEAN,
    controlled BOOLEAN,
    startTemp INT
);

CREATE TABLE system2 (
    timestamp DATETIME(3) DEFAULT CURRENT_TIMESTAMP(3) PRIMARY KEY,
    soilMoisture DECIMAL(5,2),
    temperature DECIMAL(4,1),
    humidity DECIMAL(4,1),
    moistureValue INT
);

CREATE TABLE system3 (
    timestamp DATETIME(3) DEFAULT CURRENT_TIMESTAMP(3) PRIMARY KEY,
    temperature FLOAT,
    city VARCHAR(100),
    source ENUM('button', 'motionSensor')
);

