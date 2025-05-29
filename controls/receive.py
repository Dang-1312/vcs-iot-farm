import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
import logging

import control

logging.basicConfig(filename='/home/pi/Downloads/final/envPi/publish.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# MQTT Broker Configuration
BROKER = "192.168.1.81"         # IP của máy chủ chạy Mosquitto
PORT = 1883
TOPIC = "django/publish"

status = 0  # Initial status

# Retrieve username & password from file .txt
def read_credentials(file_path):
    with open(file_path, "r") as file:
        lines = file.read().splitlines()
        if len(lines) >= 2:
            return lines[0], lines[1]  # Trả về username và password
        else:
            raise ValueError("File credentials không đúng định dạng!")
        
USERNAME, PASSWORD = read_credentials("/home/pi/Downloads/final/envPi/mqtt_credential.txt")


def report_error(error):
    retries = 0
    print(error)
    url = "http://192.168.1.81:8000/api/report_error/"
    # Error data to be sent
    error_data = {
        "error_message": str(error), # "Warning" or "Success"
        "timestamp": datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()
    }
    try:
        while retries < 3:
            # Send POST request to Django REST API
            response = requests.post(url, json=error_data)
            # Check server response
            if response.status_code == 201 or response.status_code == 200:
                print("Error report sent successfully.")
                return
            else:
                print(f"Failed to send error report. Status code: {response.status_code}")
                print(response.text)
            retries += 1
            print(f"Retrying... ({retries}/{3})")
            time.sleep(5)
        logging.warning(f"Failed to send error report after {3} attempts.")
    except requests.exceptions.RequestException as e:
        print(f"Error reporting failed: {e}")


def received(client, userdata, msg):
    global status
    try:
        print(f"Raw payload received: {msg.payload}")
        payload = json.loads(msg.payload.decode("utf-8"))
        print(f"Decoded JSON: {payload}")
    except json.JSONDecodeError:
        print("Received invalid JSON payload")
        logging.error("Received invalid JSON payload")
        return
    if payload.get("action") == "irrigation":
        print(f"Triggering irrigation with data: {payload.get('data')}")
        check_error = control.irrigate(payload.get("data"))
        print(f"Irrigation result: {check_error}")
        report_error(check_error)
    elif payload.get("action") == "mist":
        if payload.get("data") == 0:
            status = 0
        elif payload.get("data") == 1:
            status = control.mist(status)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")


def on_message(client, userdata, msg):
    logging.info(f"Received message on topic {msg.topic}")
    received(client, userdata, msg)


def main():
    global status
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.username_pw_set(USERNAME, PASSWORD) 
    client.connect(BROKER, PORT, 60)
    
    client.loop_start()

    time.sleep(5)

    while True:
        if not client.is_connected():
            try:
                client.reconnect()
                print("Reconnected to MQTT Broker")
            except Exception as e:
                print(f"Reconnect failed: {e}")
        # Check datetime and reset "status"
        now = datetime.now()
        h = now.hour
        if not 11 <= h < 14:
            if status != 0:
                status = 0
        time.sleep(60)  # Wait 60 seconds

if __name__ == "__main__":
    main()
