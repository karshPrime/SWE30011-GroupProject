import paho.mqtt.client as mqtt

# === MQTT Configuration ===
MQTT_BROKER = '169.254.176.157'           # Set to 0.0.0.0 if this script runs on broker host
MQTT_PORT = 1883
TOPIC_SUB = 'topic/example'       # Edge uploads data here
TOPIC_PUB = 'topic/command'       # Cloud sends command back to edge

# === Callback when connected ===
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker successfully")
        client.subscribe(TOPIC_SUB)
    else:
        print(f"Failed to connect: {rc}")

# === Callback when message is received ===
def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8').strip()
    print(f"Received from Edge: {payload}")

    # --- Modify or forward the command (here we just echo it back) ---
    command = payload  # In practice you could change this

    print(f"Sending to Edge: {command}")
    client.publish(TOPIC_PUB, command)

# === Setup MQTT client ===
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

# === Blocking loop to process MQTT ===
try:
    print("Cloud controller running...")
    client.loop_forever()
except KeyboardInterrupt:
    print("Stopped.")
