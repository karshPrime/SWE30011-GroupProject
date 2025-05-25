import serial
import pymysql

device = '/dev/ttyACM0'
arduino = serial.Serial(device, 9600)

try:
    #Setup DB connection
    dbconn = pymysql.connect(host="localhost", user="pi", password="", database="air_conditioning_system")
    print("Connected to database.")

    cursor = dbconn.cursor()
    while True:
        data = arduino.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {data}")

        # Temperature Reading
        if data.startswith("Temperature:"):
            temperature_value = float(data.split(":")[1])
            cursor = dbconn.cursor()
            cursor.execute("INSERT INTO temperature_readings (temperature) VALUES (%s)", (temperature_value,))
            dbconn.commit()
            print(f"Temperature inserted: {temperature_value}")

        # Temperature Control
        elif data.startswith("Temperature Control:"):
            temperature_control = bool(int(data.split(":")[1].strip()))
            cursor = dbconn.cursor()
            cursor.execute("UPDATE motor_control SET controlled = %s", (temperature_control,))
            dbconn.commit()
            print(f"Temperature control updated: {temperature_control}")

        # Set Start Temperature
        elif data.startswith("Set start temperature:"):
            start_temp_value = int(data.split(":")[1])
            cursor = dbconn.cursor()
            cursor.execute("UPDATE motor_control SET startTemp = %s", (start_temp_value,))
            dbconn.commit()
            print(f"Start temperature: {start_temp_value}.  This value is not stored in the database.")

        # Motor Override
        elif data.startswith("Motor Override:"):
            override_motor = bool(int(data.split(":")[1].strip()))
            cursor = dbconn.cursor()
            cursor.execute("UPDATE motor_control SET motorOverride = %s", (override_motor,))
            dbconn.commit()
            print(f"Motor override updated: {override_motor}")

except pymysql.MySQLError as e:
    print(f"Database error: {e}")

finally:
    if dbconn:
        dbconn.close()
