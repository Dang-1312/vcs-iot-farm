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
import read_wd5
import read_rtu as rika
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

    
# Function to check if it's time to water the plants (8:00 AM)
def check_on():
    now=datetime.datetime.now()
    h=now.hour
    m=now.minute
    if (h==9 and 10<=m<=30):
        return 1
    else:
        return 0    

# Declare parameters and connect to the sensors
# CO2 sensor RK300-03
register_address_1 = 0x00
num_registers_1 = 0x01
slave_address_1 = 0x01

# Atmospheric sensor RK330-01
register_address_2 = 0x00
num_registers_2 = 0x02
slave_address_2 = 0x02

# pH sensor RK500-02
register_address_3 = 0x00
num_registers_3 = 0x01
slave_address_3 = 0x03

# Create file log
logging.basicConfig(filename='/home/pi/Downloads/Phase_1/phase_1.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Main loop program
    while True:
        # Start time
        time_now()
        start=time.time()
        
        
        # Measure and log CPU temperature to a .log file
        cpu = measure_temp()
        log_entry = f'CPU Temperature: {cpu} °C'
        logging.info(log_entry)
        
        # Measure CO2 sensor RK300-03
        logging.info("Start measure CO2 Sensor")
        data = rika.read_sensor_rtu(register_address_1,num_registers_1,slave_address_1)
        if data[0] == "ERROR":
            logging.warning("CO2 failed")
            logging.info("Resetting sensors's power")
            extra.reset_sensor()
            CO2 = rika.read_sensor_rtu(register_address_1,num_registers_1,slave_address_1)[0]
        else:
            CO2 = data[0]
        time.sleep(1)
        
        # Measure Atmospheric sensor RK330-01
        logging.info("Start measure Atmospheric Sensor")
        Atmostpheric_data = rika.read_sensor_rtu(register_address_2,num_registers_2,slave_address_2)
        if Atmostpheric_data[0] == "ERROR":
            logging.warning("Atmostpheric failed")
            logging.info("Resetting sensors's power")
            extra.reset_sensor()  
            Atmostpheric_data = rika.read_sensor_rtu(register_address_2,num_registers_2,slave_address_2)  
            Temperature_Air = Atmostpheric_data[0]/10
            Humidity_Air = Atmostpheric_data[1]/10    
        else:
            Temperature_Air = Atmostpheric_data[0]/10
            Humidity_Air = Atmostpheric_data[1]/10
        time.sleep(1)
        
        # Measure pH sensor RK500-02
        logging.info("Start measure pH Sensor")
        data = rika.read_sensor_rtu(register_address_3,num_registers_3,slave_address_3)
        if data[0] == "ERROR":
            logging.warning("pH failed")
            logging.info("Resetting sensors's power")
            extra.reset_sensor()
            pH = rika.read_sensor_rtu(register_address_1,num_registers_1,slave_address_1)[0]/100
        else:
            pH = data[0]/100
        time.sleep(1)
        
        # Measure moisture sensor WD5
        logging.info("Start measure WD5 Sensor")
        data_wd5 = read_wd5.main_read(1)
        Vol = float(data_wd5[0])
        EC = float(data_wd5[1])
        Temp = float(data_wd5[2])
        
        # Build message for publish to cloud
        message = {
                    "Temp_air": Temperature_Air,
                    "Hum_air": Humidity_Air,
                    "CO2": CO2,
                    "pH": pH,
                    "Moisture_soil": Vol,
                    "EC": EC,
                    "Temperature_soil": Temp,
                }
        print(message)
        logging.info("Dictionary: %s", json.dumps(message))
        
        MQTT_publish.publish_data(message)
        logging.info("Success publish")      
          
        time_now()
        
        # Auto watering (Demo)
        if check_on() == 1:
            if Vol<=65:
                list=watering.main(Vol)
                logging.info("Success irregate plants")
         
        # Wait 5 minute
        end=time.time()
        wait=300+start-end
        if wait > 0 :
            time.sleep(wait)
        else:
            time.sleep(3)
            
except Exception as error: 
    # Handle the exception              
    print("An error occurred:", type(error).__name__, "–", error)              
    logging.error(f"An error occurred: {type(error).__name__} - {error}")
    