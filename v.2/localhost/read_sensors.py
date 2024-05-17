import time

import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

# Import my code
import read_wd5

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


def read_sensor_rtu(client, register_address,num_registers,slave_address):
    # Send request to device and wait return
    response = client.read_holding_registers(register_address,num_registers,slave_address)
    
    # Check error and correct data
    if not response.isError():
        list_data = response.registers
        print(list_data)
        time.sleep(1)
    else:
        if num_registers == 0x01:
            list_data = [0]
            print(list_data)
        else:
            list_data = [0,0]
            print(list_data)
    return list_data
  
def value():
    # Connect to RTU sensors
    client = ModbusClient.ModbusSerialClient(
                                            port= "/dev/ttyS0", 
                                            framer= ModbusRtuFramer,
                                            baudrate=9600,
                                            bytesize=8,
                                            parity="N",
                                            stopbits=1,
                                            errorcheck="crc",
                                            timeout=45,
                                            retries=3,
                                            )

    # Connect to RTU sensors
    connection = client.connect()
    print(f"connection: {connection}")
    
    # Measure CO2 sensor RK300-03
    CO2 = read_sensor_rtu(client, register_address_1, num_registers_1, slave_address_1)[0]
    time.sleep(1)
    
    # Measure Atmospheric sensor RK330-01
    Atmostpheric_data = read_sensor_rtu(client, register_address_2,num_registers_2,slave_address_2)
    Temperature_Air = Atmostpheric_data[0]/10
    Humidity_Air = Atmostpheric_data[1]/10
    time.sleep(1)
    
    # Measure pH sensor RK500-02
    pH = read_sensor_rtu(client, register_address_3,num_registers_3,slave_address_3)[0] /100
    time.sleep(1)
    
    client.close()
    
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
    return message  
    