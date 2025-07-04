import time
from datetime import datetime
from zoneinfo import ZoneInfo
import json
import psycopg2
import logging
import paho.mqtt.client as mqtt

import subprocess

import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus import pymodbus_apply_logging_config

import read_rtu as rs485


# MQTT broker's IP address (Mosquitto)
BROKER_IP = "192.168.1.81"
BROKER_PORT = 1883  
TOPIC = "raspi/publish"  
# client_id = f'Pi_publish-{random.randint(0, 1000)}'

# Retrieve username & password from file .txt
def read_credentials(file_path):
    with open(file_path, "r") as file:
        lines = file.read().splitlines()
        if len(lines) >= 2:
            return lines[0], lines[1]  # Trả về username và password
        else:
            raise ValueError("File credentials không đúng định dạng!")
        
USERNAME, PASSWORD = read_credentials("/home/pi/Downloads/final/envPi/mqtt_credential.txt")

# Function to connect to MQTT broker and publish a message 
def publish_data(msg):
    client = mqtt.Client(client_id="RasPi_publish") # Create a new MQTT client
    client.username_pw_set(USERNAME, PASSWORD)      # Set up username & password
    client.connect(BROKER_IP, BROKER_PORT)          # Connect to the broker
    client.loop_start()
    time.sleep(5)
    while not client.is_connected():                # Check connect
        print("Trying to connect...")
        time.sleep(3)
        client.reconnect()
    msg = json.dumps(msg)
    result = client.publish(TOPIC, msg)             # Publish the message to the topic
    while result.rc != mqtt.MQTT_ERR_SUCCESS:
        result = client.publish(TOPIC, msg)
    client.loop_stop()  
    client.disconnect()
    return result
    

# Ham kiem tra nhiet do CPU
def measure_temp():
    result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    temp_str = result.stdout.strip()
    temp = temp_str.split('=')[1].split("'")[0]
    return temp

# Create file log
# pymodbus_apply_logging_config("DEBUG")
logging.basicConfig(filename='/home/pi/Downloads/final/envPi/publish.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    status = "off"
    # Main loop program
    while True:
        # Start time
        start=time.time()
        
        # Measure and log CPU temperature to a .log file
        cpu = measure_temp()
        log_entry = f'CPU Temperature: {cpu} °C'
        logging.info(log_entry)
        
        # Measure enviromental parameters
        # Measure Soil 7in1 sensor
        # Measure Soil Moisture & Temperature
        logging.info("Start measure Soil Moisture & Temperature")
        data = rs485.read_sensor_rtu(register_address=0x12,num_registers=0x02,slave_address=0x01)
        mois_soil = min(round((data[0]/10*1.88), 1), 100)       # *532-1.88*
        temp_soil = data[1]/10
        time.sleep(1)
        
        # Measure Soil EC
        logging.info("Start measure Soil electrical conductivity value")
        data = rs485.read_sensor_rtu(register_address=0x15,num_registers=0x01,slave_address=0x01)
        ec = data[0]
        time.sleep(1)
        
        # Measure Soil NPK
        logging.info("Start measure Soil NPK")
        data = rs485.read_sensor_rtu(register_address=0x1E,num_registers=0x03,slave_address=0x01)
        N = data[0]
        P = data[1]
        K = data[2]
        time.sleep(1)
        
        # Measure Soil pH
        logging.info("Start measure Soil pH")
        data = rs485.read_sensor_rtu(register_address=0x06,num_registers=0x01,slave_address=0x01)
        pH = data[0]/100
        if pH < 4.5:
            pH = round((pH*1.7),2)
        time.sleep(1)
        
        # Measure Rika's sensors
        # Measure CO2 sensor RK300-03
        logging.info("Start measure CO2 Sensor")
        data = rs485.read_sensor_rtu(register_address=0x00,num_registers=0x01,slave_address=0x02)
        CO2 = data[0]
        time.sleep(1)
        
        # Measure Atmospheric sensor RK330-01
        logging.info("Start measure Atmospheric Sensor")
        data = rs485.read_sensor_rtu(register_address=0x00,num_registers=0x02,slave_address=0x03) 
        Temperature_Air = data[0]/10
        Humidity_Air = data[1]/10
        time.sleep(1)
         
        # Build message for publish to broker
        message = {
                    "soil_moisture": mois_soil,
                    "soil_temperature": temp_soil,
                    "ec": ec,
                    "soil_nitrogen" : N,
                    "soil_phosphorus" : P,
                    "soil_potassium" : K,
                    "ph" : pH,
                    "co2": CO2,
                    "temp_air": Temperature_Air,
                    "hum_air": Humidity_Air,  
                    "timestamp": datetime.now(ZoneInfo("Asia/Ho_Chi_Minh")).isoformat()          
                }
        print(message)
        logging.info("Dictionary: %s", json.dumps(message))     
         
        publish_data(message)

        # Wait 10 minute
        end=time.time()
        wait=600+start-end
        if wait > 0 :
            time.sleep(wait)
        else:
            time.sleep(3)
            
except Exception as error: 
    # Handle the exception              
    print("An error occurred:", type(error).__name__, "–", error)              
    logging.error(f"An error occurred: {type(error).__name__} - {error}")
    