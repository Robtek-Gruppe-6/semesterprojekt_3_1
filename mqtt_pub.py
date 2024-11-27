import paho.mqtt.client as mqtt
import json

# Define MQTT connection details
MQTT_SERVER = "localhost"  # Replace with your MQTT server address
MQTT_PORT = 1883           # Replace with your MQTT server port
MQTT_TOPIC = "mqtt_vel"  # Replace with your MQTT topic

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker successfully.")
    else:
        print(f"Failed to connect to MQTT broker, return code: {rc}")

def publish_command(linear_x, angular_z):
    # Prepare the payload to match a Twist message structure
    payload = {
        "linear": {
            "x": linear_x,
            "y": 0.0,
            "z": 0.0
        },
        "angular": {
            "x": 0.0,
            "y": 0.0,
            "z": angular_z
        }
    }
    
    # Publish the payload to the MQTT topic
    client.publish(MQTT_TOPIC, json.dumps(payload))
    print(f"Published to {MQTT_TOPIC}: {payload}")

# Initialize the MQTT client
client = mqtt.Client()
client.on_connect = on_connect

def start_mqtt():
    # Connect to the MQTT server
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.loop_start()

def stop_mqtt():
    client.loop_stop()
    client.disconnect()
    print("Disconnected from MQTT broker.")