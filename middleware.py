import threading
import time
import datetime
import json
import requests
import logging
import queue
import paho.mqtt.client as mqtt

received_count = 0
received_all_event = threading.Event()

# Configure logging
logging.basicConfig(filename='/home/ubuntu-server/Desktop/logging/Middleware.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Queue to store unsent data
unsent_data_queue = queue.Queue()


# MQTT broker's IP address (Mosquitto)
BROKER = "192.168.1.81"                                 
PORT = 1883  
TOPIC = "raspi/publish"  

# Retrieve username & password from file .txt
def read_credentials(file_path):
    with open(file_path, "r") as file:
        lines = file.read().splitlines()
        if len(lines) >= 2:
            return lines[0], lines[1]  # Return username and password
        else:
            raise ValueError("Error: File credentials are in an incorrect format!")        
USERNAME, PASSWORD = read_credentials("/home/ubuntu-server/Documents/mqtt_credential.txt")


# API endpoint for Django backend
api_url = "http://localhost:8000/api/sensor_data/"      


# Function to send data to the Django API
def post_data(msg):
    # print(msg)
    # print(type(msg))
    # response = requests.post(api_url, msg)
    # print(response.json())
    # print(response.status_code)
    global unsent_data_queue
    try:
        response = requests.post(api_url, json=msg, timeout=5)  # 5 seconds timeout
        if response.status_code == 201:
            print(f"Data sent successfully: {msg}")
            logging.info(f"Data sent successfully: {msg}")
        else:
            print(f"HTTP error {response.status_code}: {response.text}")
            logging.warning(f"HTTP error {response.status_code}: {response.text}")
            unsent_data_queue.put(msg)  # Add failed data to queue
    except requests.exceptions.RequestException as e:
        logging.error(f"API connection error: {e}")
        unsent_data_queue.put(msg)  # Add to queue if network error occurs

# Function to retry sending unsent data from the queue
def retry_unsent_data():
    while True:
        if not unsent_data_queue.empty():
            response = requests.get("http://localhost:8000/api/sensor_data/", timeout=5)  # 5 seconds timeout
            if response.status_code == 200:
                data = unsent_data_queue.get()
                logging.info(f"Retrying to send data: {data}")
                post_data(data)
            else:
                logging.warning(f"Cannot retry sending data due to error: {response.status_code}")
        time.sleep(10)  # Check every 10 seconds

# MQTT on_connect callback function
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(TOPIC)
    else:
        print(f"Failed to connect, return code {rc}")

# MQTT on_message callback function
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode("utf-8"))
    post_data(payload)

# Main function to start MQTT client
def main():
    global status
    client = mqtt.Client()                      # Create a new MQTT client
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set(USERNAME, PASSWORD)  # Set up username & password
    client.connect(BROKER, PORT)            # Connect to the broker
    
    # time.sleep(3)

    # while not client.is_connected():            # Check connect
    #     print("Trying to connect...")
    #     time.sleep(3)
    #     client.reconnect()

    # Start a separate thread to retry sending failed data
    retry_thread = threading.Thread(target=retry_unsent_data, daemon=True)
    retry_thread.start()

    # Start MQTT loop
    client.loop_forever()

if __name__ == "__main__":
    main()