
# scripts/control.py

HOSTNAME = "169.254.123.100"

#- Imports -----------------------------------------------------------------------------------------

import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

#- Configurable Controls ---------------------------------------------------------------------------

s1_motor = None
s1_temperature_threshold = None
s2_moisture_threshold = None
s3_temperature = None
s3_city = None
s3_source = None


#- MQTT Publish ------------------------------------------------------------------------------------

def mqtt_write1(message):
    if message:
        temp = None
        control = None
        parts = message.lower().split()

        for part in parts:
            key_value = part.split(':')
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()

                publish.single(f"/edge/s1/{key}", value, hostname=HOSTNAME)

def mqtt_write2(moisture, temperature, humidity, callibration):
    if moisture:
        publish.single("/edge/s2/moisture", moisture, hostname=HOSTNAME)
    else:
        publish.single("/edge/s2/moisture", 0, hostname=HOSTNAME)


    if temperature:
        publish.single("/edge/s2/temperature", temperature, hostname=HOSTNAME)

    if humidity:
        publish.single("/edge/s2/humidity", humidity, hostname=HOSTNAME)

    if callibration:
        publish.single("/edge/s2/callibration", callibration, hostname=HOSTNAME)


#- MQTT Subscribe ----------------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    print("[mqtt] Connected with result code ", rc)
    client.subscribe("/cloud/s1/motor")
    client.subscribe("/cloud/s1/temperature_threshold")
    client.subscribe("/cloud/s2/moisture_threshold")
    client.subscribe("/cloud/s3/temperature")
    client.subscribe("/cloud/s3/city")
    client.subscribe("/cloud/s3/source")


def on_message(client, userdata, msg):
    message = msg.payload.decode()

    if msg.topic == "/cloud/s1/motor":
        print("[mqtt] motor set to ", message)
        global s1_motor
        s1_motor = message

    elif msg.topic == "/cloud/s1/temperature_threshold":
        print("[mqtt] temperature_threshold set to ", message)
        global s1_temperature_threshold
        s1_temperature_threshold = message

    elif msg.topic == "/cloud/s2/moisture_threshold":
        print("[mqtt] moisture_threshold set to ", message)
        global s2_moisture_threshold
        s2_moisture_threshold = message

    elif msg.topic == "/cloud/s3/temperature":
        print("[mqtt] temperature set to ", message)
        global s3_temperature
        s3_temperature = message

    elif msg.topic == "/cloud/s3/city":
        print("[mqtt] city set to ", message)
        global s3_city
        s3_city = message

    elif msg.topic == "/cloud/s3/source":
        print("[mqtt] source set to ", message)
        global s3_source
        s3_source = message

    else:
        print(f"[mqtt] invalid topic:\"{msg.topic}\" : {message}")


def mqtt_setup():
    print("[mqtt] Setting Connection")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(HOSTNAME, 1883, 60)
    client.loop_forever()


#- Get Values --------------------------------------------------------------------------------------

def get_s1_message():
    global s1_motor
    if s1_motor:
        value = s1_motor
        s1_motor = None
        return value

    global s1_temperature_threshold
    if s1_temperature_threshold:
        value = s1_temperature_threshold
        s1_temperature_threshold = None

        return f"t{value}"


def get_s2_moisture_threshold():
    global s2_moisture_threshold
    value = s2_moisture_threshold
    s2_moisture_threshold = None # prevent from data repeat
    return value


def get_s3_data():
    global s3_source

    temperature = s3_temperature or ""
    city = s3_city or ""

    source = ""

    if s3_source == "MS":
        source = "motionSensor"
    elif s3_source == "BT":
        source = "button"

    s3_source = None

    return (temperature, city, source)

#---------------------------------------------------------------------------------------------------

