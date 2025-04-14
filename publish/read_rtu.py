import time

import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
# from pymodbus import pymodbus_apply_logging_config

import sys
sys.path.append('/home/pi/Downloads/final/envPi')

from controls import extra
import logging

    
def read_sensor_rtu(register_address,num_registers,slave_address):
    rtu_client = ModbusClient.ModbusSerialClient(
                                            port= "/dev/ttyS0", 
                                            framer= ModbusRtuFramer,
                                            baudrate=9600,
                                            bytesize=8,
                                            parity="N",
                                            stopbits=1,
                                            errorcheck="crc",
                                            timeout=45,
                                            retries=2,
                                            retry_on_empty=True,
                                            )

    list_data = None
    
    # Connect to RS485 device
    connection = rtu_client.connect()
    print(f"connection {slave_address}: {connection}")

    # Send request to device and wait return
    response = rtu_client.read_holding_registers(register_address,num_registers,slave_address)
    
    # Check error
    if not response.isError():
        list_data = response.registers
        print(list_data)
        time.sleep(1)
        rtu_client.close()
        return list_data 
    else:
        rtu_client.close()
        extra.reset_sensor()
        list_data = read_sensor_rtu(register_address,num_registers,slave_address)    
        print(list_data)
        rtu_client.close()     
        return list_data 
    