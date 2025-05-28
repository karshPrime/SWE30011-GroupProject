
# scripts/board.py

BROKER = "mqtt.thingsboard.cloud"
USERNAME = "vO6gCzuC6OUOoQifsTAN"

#- Imports -----------------------------------------------------------------------------------------

import paho.mqtt.client as mqtt
import serial
import time

client = mqtt.Client()


#- MQTT Publish ------------------------------------------------------------------------------------

def thingsboard_publish( tag, value ):
    client.publish("v1/devices/me/telemetry", f'{{"{tag}":{value}}}')


#- MQTT Subscribe ----------------------------------------------------------------------------------

def thingsboard_setup():
    print("[thingsboard] Setting Connection")
    client.username_pw_set(USERNAME)
    client.connect(BROKER, 1883, 60)
    client.loop_start()

def thingsboard_terminate():
    client.loop_stop()
    client.disconnect()

