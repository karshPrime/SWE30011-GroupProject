
# scripts/system.py

#- Imports -----------------------------------------------------------------------------------------

import time
import serial
import requests

from .control import mqtt_write3, s2_moisture_alert
from .board   import thingsboard_publish

#- Get Weather -------------------------------------------------------------------------------------

CITY = "Melbourne"
TEMPERATURE = None
STOP = False

def request_city_temperature(city):
    global TEMPERATURE
    response = requests.get( f"https://wttr.in/{city}?format=3" )

    if response.status_code == 200:
        full_text = response.text     # e.g. "Melbourne: 🌦 +18°C"
        TEMPERATURE = full_text.split()[-1].replace("°C", "")

        mqtt_write3("temperature", TEMPERATURE)
        mqtt_write3("city", city)

        thingsboard_publish("s3_temperature", TEMPERATURE)
        thingsboard_publish("s3_city", city)

        return True
    else:
        print("[system] Failed to get weather data for {city}")
        return False

def get_temperature(newCity):
    global CITY
    if request_city_temperature(newCity):
        CITY = newCity
    else:
        request_city_temperature(CITY)

def update_temperature():
    while True:
        request_city_temperature(CITY)
        time.sleep(300) # 300 seconds; 5mins


#- Public Calls ------------------------------------------------------------------------------------

def system_run(port):
    global TEMPERATURE

    with serial.Serial( port, 9600, timeout=1 ) as connection:
        time.sleep( 2 )
        print( "[system] setting up system3" )

        while True:
            thingsboard_publish(f"s3_MS", 0)
            thingsboard_publish(f"s3_BT", 0)

            # --- Prepare message from control ---
            if TEMPERATURE:
                connection.write(f"LCD:{CITY}={TEMPERATURE}".encode('utf-8') + b'\n')
                TEMPERATURE = None

            if s2_moisture_alert():
                connection.write("alert".encode('utf-8') + b'\n')

            # --- Read response from Arduino ---
            if connection.in_waiting > 0:
                line = connection.readline().decode('utf-8').strip()

                mqtt_write3( "source", line );
                thingsboard_publish(f"s3_{line}", 1)

            if STOP:
                break

            time.sleep(1)

def system_terminate():
    global STOP
    STOP = True

