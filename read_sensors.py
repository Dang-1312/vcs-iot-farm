import time
import datetime
import json
import psycopg2
import logging

import subprocess

import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus import pymodbus_apply_logging_config

# import my code
# import read_wd5
import read_rtu as rs485
import control_main as watering
import MQTT_publish
import control_extra as extra

# Ham in ra time now
def time_now():
    d = datetime.datetime.now()
    print(d.strftime('%Y/%m/%d %H:%M:%S'))


# Ham kiem tra nhiet do CPU
def measure_temp():
    result = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True, text=True)
    temp_str = result.stdout.strip()
    temp = temp_str.split('=')[1].split("'")[0]
    return temp


# Create file log
# pymodbus_apply_logging_config("DEBUG")
logging.basicConfig(filename='/home/pi/Downloads/Phase_2/phase_2.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    status = "off"
    # Main loop program
    while True:
        # Start time
        time_now()
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
        if data[0] == "ERROR":
            logging.warning("Soil moisture & temperature failed")
            logging.info("Resetting sensors's power")
            extra.reset_sensor()
            data = rs485.read_sensor_rtu(register_address=0x12,num_registers=0x02,slave_address=0x01)  
        mois_soil = data[0]/10
        temp_soil = data[1]/10
        time.sleep(1)
        
        # Measure Soil EC
        logging.info("Start measure Soil electrical conductivity value")
        data = rs485.read_sensor_rtu(register_address=0x15,num_registers=0x01,slave_address=0x01)
        if data[0] == "ERROR":
            logging.warning("EC failed")
            logging.info("Resetting sensors's power")
            extra.reset_sensor()
            data = rs485.read_sensor_rtu(register_address=0x15,num_registers=0x01,slave_address=0x01)
        ec = data[0]
        time.sleep(1)
        
        # Measure Soil NPK
        logging.info("Start measure Soil NPK")
        data = rs485.read_sensor_rtu(register_address=0x1E,num_registers=0x03,slave_address=0x01)
        if data[0] == "ERROR":
            logging.warning("NPK failed")
            logging.info("Resetting sensors's power")
            extra.reset_sensor()
            data = rs485.read_sensor_rtu(register_address=0x1E,num_registers=0x03,slave_address=0x01)
        N = data[0]
        P = data[1]
        K = data[2]
        time.sleep(1)
        
        # Measure Soil pH
        logging.info("Start measure Soil pH")
        data = rs485.read_sensor_rtu(register_address=0x06,num_registers=0x01,slave_address=0x01)
        if data[0] == "ERROR":
            logging.warning("EC failed")
            logging.info("Resetting sensors's power")
            extra.reset_sensor()
            data = rs485.read_sensor_rtu(register_address=0x06,num_registers=0x01,slave_address=0x01)
        pH = data[0]/100
        time.sleep(1)
        
        # Measure Rika's sensors
        # Measure CO2 sensor RK300-03
        logging.info("Start measure CO2 Sensor")
        data = rs485.read_sensor_rtu(register_address=0x00,num_registers=0x01,slave_address=0x02)
        if data[0] == "ERROR":
            logging.warning("CO2 failed")
            logging.info("Resetting sensors's power")
            extra.reset_sensor()
            data = rs485.read_sensor_rtu(register_address=0x00,num_registers=0x01,slave_address=0x02)
        CO2 = data[0]
        time.sleep(1)
        
        # Measure Atmospheric sensor RK330-01
        logging.info("Start measure Atmospheric Sensor")
        data = rs485.read_sensor_rtu(register_address=0x00,num_registers=0x02,slave_address=0x03)
        if data[0] == "ERROR":
            logging.warning("Atmostpheric failed")
            logging.info("Resetting sensors's power")
            extra.reset_sensor()  
            data = rs485.read_sensor_rtu(register_address=0x00,num_registers=0x02,slave_address=0x03)  
        Temperature_Air = data[0]/10
        Humidity_Air = data[1]/10
        time.sleep(1)
         
        # Build message for publish to cloud
        message = {
                    "Moisture_soil": mois_soil,
                    "Temperature_soil": temp_soil,
                    "EC": ec,
                    "Soil_nitrogen" : N,
                    "Soil_phosphorus" : P,
                    "Soil_potassium" : K,
                    "pH" : pH,
                    "CO2": CO2,
                    "Temp_air": Temperature_Air,
                    "Hum_air": Humidity_Air,                   
                }
        print(message)
        logging.info("Dictionary: %s", json.dumps(message))
        
        mqtt_status = MQTT_publish.publish_data(message)
        logging.info(f"MQTT status: {mqtt_status}")      
          
        time_now()
        
        # Auto watering (Demo)
        now=datetime.datetime.now()
        h=now.hour
        m=now.minute
        if (h==9 and 15<=m<=45) and (mois_soil<=60):
            watering.main(mois_soil)
            logging.info("Success irregate plants")
            
        if (11<=h<14) and (Temperature_Air>=33 or Humidity_Air<=55) and status == "off":
            status = watering.air(status, 1)
            logging.info("Misting in progress")
        elif status == "on" and (Temperature_Air>=33 or Humidity_Air<=55):
            status = watering.air(status, 1)
            logging.info("Misting in progress")
        elif status == "on":
            status = watering.air(status, 2)
            logging.info("Misting completed")
         
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
    