
# scripts/system.py

#- Imports -----------------------------------------------------------------------------------------

import time
import serial
import requests

from .control import mqtt_write3

#- Get Weather -------------------------------------------------------------------------------------

CITY = "Melbourne"
TEMPERATURE = None

def request_city_temperature(city):
    global TEMPERATURE
    response = requests.get( f"https://wttr.in/{city}?format=3" )

    if response.status_code == 200:
        full_text = response.text     # e.g. "Melbourne: 🌦 +18°C"
        TEMPERATURE = full_text.split()[-1].replace("°C", "")
        mqtt_write3("temperature", TEMPERATURE)
        mqtt_write3("city", city)
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
            # --- Prepare message from control ---
            if TEMPERATURE:
                connection.write(f"LCD:{CITY}={TEMPERATURE}".encode('utf-8') + b'\n')
                TEMPERATURE = None

            # --- Read response from Arduino ---
            if connection.in_waiting > 0:
                line = connection.readline().decode('utf-8').strip()

                mqtt_write3( "source", line );

            time.sleep(1)

