import time

import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
# from pymodbus import pymodbus_apply_logging_config

import logging

    
def read_sensor_rtu(register_address,num_registers,slave_address):
    # logging.basicConfig(filename='phase_1.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    # pymodbus_apply_logging_config("DEBUG")
    client = ModbusClient.ModbusSerialClient(
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
    connection = client.connect()
    print(f"connection {slave_address}: {connection}")

    # Send request to device and wait return
    response = client.read_holding_registers(register_address,num_registers,slave_address)
    
    # Check error
    if not response.isError():
        list_data = response.registers
        print(list_data)
        time.sleep(1)
        client.close()
        return list_data 
    else:
        logging.info("Measurement ERROR from RS485 sensor.")
        client.close()
        return ["ERROR"]         
    