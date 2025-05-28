
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

def on_connect(client, userdata, flags, rc):
    print("[thingsboard] Connected with result code", rc)

def on_message(client, userdata, msg):
    print("[thingsboard] " + msg.topic + ": " + str(msg.payload))

def thingsboard_setup():
    print("[thingsboard] Setting Connection")
    client.username_pw_set(USERNAME)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, 1883, 60)
    client.loop_start()

def thingsboard_terminate():
    client.loop_stop()
    client.disconnect()

