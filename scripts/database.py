
# scripts/database.py

import time
import pymysql

#- Global ------------------------------------------------------------------------------------------

DBConnection = pymysql.connect(
    host="localhost",
    user="edge",
    passwd="",
    db="assignment3"
)
Cursor = DBConnection.cursor()


#- System1 Queries ---------------------------------------------------------------------------------

def database_write1(prompt):
    if prompt.startswith("Temperature:"):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        temperature_value = float(prompt.split(":")[1])
        Cursor.execute(
            "INSERT INTO system1 (timestamp, temperature) VALUES (%s, %s)",
            (now, temperature_value)
        )

    elif prompt.startswith("Temperature Control:"):
        temperature_control = bool(int(prompt.split(":")[1].strip()))
        Cursor.execute(
            "UPDATE system1 SET controlled = %s ORDER BY timestamp DESC LIMIT 1",
            (temperature_control,)
        )

    elif prompt.startswith("Set start temperature:"):
        start_temp_value = int(prompt.split(":")[1])
        Cursor.execute(
            "UPDATE system1 SET startTemp = %s ORDER BY timestamp DESC LIMIT 1",
            (start_temp_value,)
        )

    elif prompt.startswith("Motor Override:"):
        override_motor = bool(int(prompt.split(":")[1].strip()))
        Cursor.execute(
            "UPDATE system1 SET motorOverride = %s ORDER BY timestamp DESC LIMIT 1",
            (override_motor,)
        )

    DBConnection.commit()

#---------------------------------------------------------------------------------------------------

