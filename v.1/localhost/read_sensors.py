import time
import datetime
import json
import psycopg2


import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus import pymodbus_apply_logging_config

# import my code
import read_wd5
import read_rtu as rika
import aws_iot_trans as aws
import control_watering as watering

# Ham in ra time now
def time_now():
    d = datetime.datetime.now()
    print(d.strftime('%Y/%m/%d %H:%M:%S'))
    

# Khai bao thong so va connect voi cac sensors
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


# Main loop program
while True:
    # Start time
    time_now()
    start=time.time()
    

    # Measure CO2 sensor RK300-03
    CO2 = rika.read_sensor_rtu(register_address_1,num_registers_1,slave_address_1,0)[0]
    time.sleep(1)
    
    # Measure Atmospheric sensor RK330-01
    Atmostpheric_data = rika.read_sensor_rtu(register_address_2,num_registers_2,slave_address_2,0)
    Temperature_Air = Atmostpheric_data[0]/10
    Humidity_Air = Atmostpheric_data[1]/10
    time.sleep(1)
    
    # Measure pH sensor RK500-02
    pH = rika.read_sensor_rtu(register_address_3,num_registers_3,slave_address_3,0)[0] /100
    time.sleep(1)
    
    # Measure moisture sensor WD5
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
    
    
    # Publish data to AWS IoT Broker
    
    time_now()
    
    
    # Check request and run control_watering
    pl = aws.receive()          # Receive payload from aws iot broker
    if not pl == None :         # Check payload request 
        list = pl
    
    if Vol<=60:
        list=watering.watering(list[0],list[1],list[2])
    
    
    # Wait 5 minute
    end=time.time()
    wait=300+start-end
    if wait > 0 :
        time.sleep(wait)     
    