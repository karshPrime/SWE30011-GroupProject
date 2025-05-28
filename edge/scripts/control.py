
# scripts/control.py

HOSTNAME = "169.254.123.100"

import paho.mqtt.client as mqtt
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


#- MQTT Subscribe ----------------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    print("[mqtt] Connected with result code " + str(rc))
    client.subscribe("/cloud/s1/motor")
    client.subscribe("/cloud/s1/temperature_threshold")
    client.subscribe("/cloud/s2/moisture_threshold")
    client.subscribe("/cloud/s3/temperature")
    client.subscribe("/cloud/s3/button")
    client.subscribe("/cloud/s3/motionSensor")


def on_message(client, userdata, msg):
    message = msg.payload.decode()

    if msg.topic == "/cloud/s1/motor":
        global s1_motor
        s1_motor = message

    elif msg.topic == "/cloud/s1/temperature_threshold":
        global s1_temperature_threshold
        s1_temperature_threshold = message

    elif msg.topic == "/cloud/s2/moisture_threshold":
        global s2_moisture_threshold
        s2_moisture_threshold = message

    elif msg.topic == "/cloud/s3/temperature":
        global s3_temperature
        s3_temperature = message

    elif msg.topic == "/cloud/s3/button":
        global s3_button
        s3_button = message

    elif msg.topic == "/cloud/s3/motionSensor":
        global s3_motionSensor
        s3_motionSensor = message

    else:
        print(f"[mqtt] invalid topic:\"{msg.topic}\" : {message}")


def mqtt_setup():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOSTNAME, 1883, 60)
    client.loop_forever()


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

