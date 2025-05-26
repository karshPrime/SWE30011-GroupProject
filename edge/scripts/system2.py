
# scripts/system2.py

#- Imports -----------------------------------------------------------------------------------------

import time
import serial

from .control  import get_s2_moisture_threshold, mqtt_write2
from .database import database_write2


#- Public Calls ------------------------------------------------------------------------------------

def Run(port):
    with serial.Serial(port, 9600, timeout=1) as connection:
        time.sleep(2)
        print("[system2] setting up system2")

        while True:
            values = {
                'moisture': None,
                'temperature': None,
                'humidity': None,
                'callibration': None
            }

            # Read 4 lines of data (moisture, temp, humidity, callibration)
            for _ in range(4):
                if connection.in_waiting > 0:
                    line = connection.readline().decode('utf-8').strip()

                    if ':' in line:
                        key, value = line.split(':')
                        key = key.strip()
                        value = value.strip()

                        try:
                            value = float(value)
                        except ValueError:
                            print(f"[system2] Invalid value for {key}: {value}")
                            continue

                        if key in values:
                            values[key] = value
                        else:
                            print(f"[system2] Unknown key: {key}")

                    else:
                        print(f"[system2] Malformed line: {line}")

            database_write2(
                values['moisture'], values['temperature'],
                values['humidity'], values['callibration']
            )

            mqtt_write2( 
                values['moisture'], values['temperature'],
                values['humidity'], values['callibration']
            )

            # Check buzzer condition
            try:
                moisture = values['moisture']
                threshold = get_s2_moisture_threshold()

                if moisture is not None:
                    if moisture < threshold:
                        connection.write(b"1\n")
                    else:
                        connection.write(b"0\n")

            except Exception as e:
                print(f"[system2] Error in buzzer control: {e}")

            time.sleep(1)

#---------------------------------------------------------------------------------------------------

