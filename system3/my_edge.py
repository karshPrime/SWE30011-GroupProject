import serial
import time
import subprocess
import threading
import paho.mqtt.client as mqtt

# === Configuration ===
SERIAL_PORT = '/dev/ttyACM0'  # e.g., 'COM3' on Windows or '/dev/ttyACM0' on Linux
BAUD_RATE = 9600
MQTT_BROKER = '169.254.176.157'
MQTT_PORT = 1883
MQTT_PUB_TOPIC = 'topic/example'     # Topic for publishing Arduino data
MQTT_SUB_TOPIC = 'topic/command'     # Topic for receiving control commands

# === Initialize serial connection ===
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to serial port {SERIAL_PORT}")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# === MQTT Callback: on successful connection ===
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(MQTT_SUB_TOPIC)  # Subscribe to command topic
    else:
        print(f"Failed to connect, return code {rc}")

# === MQTT Callback: when message is received ===
def on_message(client, userdata, msg):
    command = msg.payload.decode('utf-8').strip()
    print(f"Received command from MQTT: {command}")
    ser.write((command + '\n').encode('utf-8'))  # Send command to Arduino via serial

# === Setup MQTT client ===
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)

# === Run MQTT client loop in a separate thread ===
def mqtt_loop():
    mqtt_client.loop_forever()

threading.Thread(target=mqtt_loop, daemon=True).start()

# === Main loop: read from Arduino serial and publish to MQTT ===
try:
    while True:
        if ser.in_waiting:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Received from Arduino: {line}")
                mqtt_client.publish(MQTT_PUB_TOPIC, line)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting program...")
finally:
    ser.close()
