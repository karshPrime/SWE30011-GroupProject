
# scripts/control.py

HOSTNAME = "169.254.123.100"

#- Imports -----------------------------------------------------------------------------------------

import time
import serial

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

from .board import thingsboard_publish


#- Trigger Alert Beep ------------------------------------------------------------------------------

s2_moisture = None
moisture_threshold = None

def s2_moisture_alert():
    try:
        return float(s2_moisture) > float(moisture_threshold)
    except:
        return False


#- MQTT Publish ------------------------------------------------------------------------------------

def mqtt_write1(topic, value):
    publish.single(f"/cloud/s1/{topic}", value, hostname=HOSTNAME)

def mqtt_write2(value):
    publish.single("/cloud/s2/moisture_threshold", value, hostname=HOSTNAME)
    global moisture_threshold
    moisture_threshold = value

def mqtt_write3(title, data):
    # temperature, city, source
    publish.single(f"/cloud/s3/{title}", data, hostname=HOSTNAME)


#- MQTT Subscribe ----------------------------------------------------------------------------------

client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("[mqtt] Connected with result code " + str(rc))
    client.subscribe("/edge/s1/temperature")
    client.subscribe("/edge/s1/control")
    client.subscribe("/edge/s2/moisture")
    client.subscribe("/edge/s2/temperature")
    client.subscribe("/edge/s2/humidity")
    client.subscribe("/edge/s2/callibration")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    topic = '_'.join(msg.topic.split('/')[-2:])

    print(f"[mqtt]\"{topic}\" : {message}")

    thingsboard_publish(topic, message)

    if topic == "s2_moisture":
        global s2_moisture
        s2_moisture = message

def mqtt_setup():
    print("[mqtt] Setting Connection")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOSTNAME, 1883, 60)
    client.loop_forever()

def mqtt_terminate():
    client.loop_stop()
    client.disconnect()


#---------------------------------------------------------------------------------------------------

