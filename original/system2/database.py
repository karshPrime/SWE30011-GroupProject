import serial
import MySQLdb
import time

device = '/dev/ttyACM0'

arduino = serial.Serial(device, 9600, timeout=1)

try:
    dbconn = MySQLdb.connect(host="localhost", user="pi", passwd="", db="assignment_db")
    print("Connected to the database")
    cursor = dbconn.cursor()

    for _ in range(10):
        values = {
            'moisture': None,
            'temperature': None,
            'humidity': None,
            'callibration': None
        }
        
        for _ in range(4):
            data = arduino.readline().decode('utf-8').strip()
            if ':' in data:
                key, value = data.split(":")
                key = key.strip()
                value = value.strip()
                try:
                    value = float(value)
                except ValueError:
                    print(f"Invalid value for {key}: {value}")
                    continue
                if key in values:
                    values[key] = value
                else:
                    print(f"Unknown key: {key}")
            else:
                print(f"Formatting invalid: {data}")

                
        cursor.execute(f"INSERT INTO sensor_data (soilMoisture, temperature, humidity, moistureValue) VALUES (%s, %s, %s, %s)", (values['moisture'], values['temperature'], values['humidity'], values['callibration']))
        dbconn.commit()
        time.sleep(2)
    
    
except MySQLdb.Error as e:
    print(f"Database error: {e}")
    
finally:
    if dbconn:
        cursor.close()
        dbconn.close()
