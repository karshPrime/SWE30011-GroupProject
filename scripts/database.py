# scripts/database.py

import time
import pymysql
import threading
import time

#- Global ------------------------------------------------------------------------------------------

DBConnection = pymysql.connect(
    host="localhost",
    user="edge",
    passwd="",
    db="assignment3"
)
Cursor = DBConnection.cursor()

# Queue for scheduled queries
scheduled_queries = []

# Lock for thread-safe queue access
from threading import Lock
queue_lock = Lock()

#- Database write scheduler ------------------------------------------------------------------------

def database_write_scheduler():
    while True:
        with queue_lock:
            if scheduled_queries:
                query, values = scheduled_queries.pop(0)
                try:
                    Cursor.execute(query, values)
                    DBConnection.commit()
                except Exception as e:
                    print( e )
                    pass  # Skipping the failed query
        time.sleep(0.01)  # Avoid 100% CPU usage

# Start scheduler in a separate thread
threading.Thread(target=database_write_scheduler, daemon=True).start()

#- System1 Queries ---------------------------------------------------------------------------------

def database_write1(prompt):
    now = time.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(int(time.time() * 1000) % 1000)

    with queue_lock:
        if prompt.startswith("Temperature:"):
            temperature_value = float(prompt.split(":")[1])
            scheduled_queries.append((
                "INSERT INTO system1 (timestamp, temperature) VALUES (%s, %s)",
                (now, temperature_value)
            ))

        elif prompt.startswith("Temperature Control:"):
            temperature_control = bool(int(prompt.split(":")[1].strip()))
            scheduled_queries.append((
                "UPDATE system1 SET controlled = %s ORDER BY timestamp DESC LIMIT 1",
                (temperature_control,)
            ))

        elif prompt.startswith("Set start temperature:"):
            start_temp_value = int(prompt.split(":")[1])
            scheduled_queries.append((
                "UPDATE system1 SET startTemp = %s ORDER BY timestamp DESC LIMIT 1",
                (start_temp_value,)
            ))

        elif prompt.startswith("Motor Override:"):
            override_motor = bool(int(prompt.split(":")[1].strip()))
            scheduled_queries.append((
                "UPDATE system1 SET motorOverride = %s ORDER BY timestamp DESC LIMIT 1",
                (override_motor,)
            ))

#- System2 Queries ---------------------------------------------------------------------------------

def database_write2(moisture, temperature, humidity, callibration):
    now = time.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(int(time.time() * 1000) % 1000)
    with queue_lock:
        scheduled_queries.append((
            "INSERT INTO system2 (timestamp, soilMoisture, temperature, humidity, moistureValue)\
             VALUES (%s, %s, %s, %s, %s)",
            (now, moisture, temperature, humidity, callibration)
        ))

#- System3 Queries ---------------------------------------------------------------------------------

def database_write3(potentiometer, button, motionSensor):
    now = time.strftime('%Y-%m-%d %H:%M:%S') + '.' + str(int(time.time() * 1000) % 1000)
    with queue_lock:
        scheduled_queries.append((
            "INSERT INTO system3 (timestamp, potentiometer, button, motionSensor)\
             VALUES (%s, %s, %s, %s)",
            (now, potentiometer, button, motionSensor)
        ))
