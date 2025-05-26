
# scripts/control.py

HOSTNAME = "169.254.123.100"

import paho.mqtt.publish as publish

#- Configurable Controls ---------------------------------------------------------------------------

s1_motor = None
s1_temperature_threshold = None
s2_moisture_threshold = None
s3_temperature = None
s3_button = None
s3_motionSensor = None


#- MQTT Publish ------------------------------------------------------------------------------------

def mqtt_write1(message):
    publish.single("/edge/s1/prompt", message, hostname=HOSTNAME)

def mqtt_write2(moisture, temperature, humidity, callibration):
    publish.single("/edge/s2/moisture", moisture, hostname=HOSTNAME)
    publish.single("/edge/s2/temperature", temperature, hostname=HOSTNAME)
    publish.single("/edge/s2/humidity", humidity, hostname=HOSTNAME)
    publish.single("/edge/s2/callibration", callibration, hostname=HOSTNAME)





#- Get Values --------------------------------------------------------------------------------------

def get_s1_message():
    if s1_motor:
        value = s1_motor

        global s1_motor
        s1_motor = None

        return value

    if s1_temperature_threshold:
        value = s1_temperature_threshold

        global s1_temperature_threshold
        s1_temperature_threshold = None

        return f"t{value}"


def get_s2_moisture_threshold():
    value = s2_moisture_threshold
    
    # prevent from data repeat
    global s2_moisture_threshold
    s2_moisture_threshold = None

    return value


def get_s3_data():
    button, temperature, motionSensor = s3_button, s3_temperature, s3_motionSensor

    global s3_button, s3_temperature, s3_motionSensor
    s3_button = None
    s3_temperature = None
    s3_motionSensor = None

    return (button, temperature, motionSensor)

#---------------------------------------------------------------------------------------------------

