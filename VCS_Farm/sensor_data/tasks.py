# sensor_data/tasks.py

from celery import shared_task
from sensor_data.models import SensorData
from standard_data.models import StandardData
import paho.mqtt.client as mqtt
import json
import time
import datetime

# MQTT broker's IP address (Mosquitto)
BROKER_IP = "192.168.1.81"
BROKER_PORT = 1883  
TOPIC = "django/publish"  

# Retrieve username & password from file .txt
def read_credentials(file_path):
    with open(file_path, "r") as file:
        lines = file.read().splitlines()
        if len(lines) >= 2:
            return lines[0], lines[1]  # Return username and password
        else:
            raise ValueError("File credentials không đúng định dạng!")

USERNAME, PASSWORD = read_credentials("/home/ubuntu-server/Documents/mqtt_credential.txt")

# Function to connect to MQTT broker and publish a message
def publish_data(msg):
    client = mqtt.Client(client_id="Django_publish")  # Create a new MQTT client 
    client.username_pw_set(USERNAME, PASSWORD)       # Set up username & password
    client.connect(BROKER_IP, BROKER_PORT)           # Connect to the broker
    client.loop_start()
    time.sleep(5)
    while not client.is_connected():                 # Check connect
        print("Trying to connect...")
        time.sleep(3)
        client.reconnect()
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)              # Publish the message to the topic
    while result.rc != mqtt.MQTT_ERR_SUCCESS:
        result = client.publish(TOPIC, msg)
    client.loop_stop()  
    client.disconnect()
    return result

@shared_task
def check_and_publish_irrigation():
    latest_sensor = SensorData.objects.latest('timestamp')
    latest_standard = StandardData.objects.latest('created_at')

    if latest_sensor.soil_moisture < latest_standard.min_soil_moisture:
        data = latest_standard.max_soil_moisture - latest_sensor.soil_moisture
        message = {"action": "irrigation", "data": round(data, 2)}
        publish_data(message)
        return f"Published: {message}"
    return "No irrigation needed."

@shared_task
def check_and_publish_mist():
    latest_sensor = SensorData.objects.latest('timestamp')
    latest_standard = StandardData.objects.latest('created_at')
    if (latest_sensor.temp_air > latest_standard.max_temperature) or (latest_sensor.hum_air < latest_standard.min_humidity):
        now=datetime.datetime.now()
        if not ((now.hour == 13) and (50 <= now.minute <=59)):
            message = {"action": "mist", "data": 1}
        else:
            message = {"action": "mist", "data": 0}
        publish_data(message)
        return f"Published: {message}"    
    return "No mist needed."
