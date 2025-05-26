
# scripts/control.py

HOSTNAME = "169.254.123.100"

import paho.mqtt.publish as publish

#- Configurable Controls ---------------------------------------------------------------------------

s1_motor = 0
s1_temperature_threshold = 25
s2_moisture_threshold = 20
s3_temperature = ""

old_s1_motor = 0
old_s1_temperature_threshold = 25
old_s3_temperature = ""


#- Public Functions --------------------------------------------------------------------------------

def get_s1_message():
    global s1_motor
    global old_s1_motor

    if s1_motor != old_s1_motor:
        old_s1_motor = s1_motor
        return "m"

    global s1_temperature_threshold
    global old_s1_temperature_threshold

    if s1_temperature_threshold != old_s1_temperature_threshold:
        old_s1_temperature_threshold = s1_temperature_threshold
        return f"t{s1_temperature_threshold}"


def clear_s1_message():
    global s1_temperature_threshold
    global old_s1_temperature_threshold

    old_s1_temperature_threshold = s1_temperature_threshold
    old_s1_motor = s1_motor


def get_s2_moisture_threshold():
    return s2_moisture_threshold


#---------------------------------------------------------------------------------------------------

def mqtt_write1(message):
    publish.single( "/system1/system1", message, hostname=HOSTNAME)

def mqtt_write2(moisture, temperature, humidity, callibration):
    publish.single( "/system2/moisture", moisture, hostname=HOSTNAME)
    publish.single( "/system2/temperature", temperature, hostname=HOSTNAME)
    publish.single( "/system2/humidity", humidity, hostname=HOSTNAME)
    publish.single( "/system2/callibration", callibration, hostname=HOSTNAME)

def UpdateValues():
    pass

