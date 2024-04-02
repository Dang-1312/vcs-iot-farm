import time

import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer
from pymodbus import pymodbus_apply_logging_config


def read_sensor_rtu(register_address,num_registers,slave_address,i):
    client = ModbusClient.ModbusSerialClient(
                                            port= "/dev/ttyS0", 
                                            framer= ModbusRtuFramer,
                                            baudrate=9600,
                                            bytesize=8,
                                            parity="N",
                                            stopbits=1,
                                            errorcheck="crc",
                                            )

    # Connect to Module RS485 to ETH (B)
    connection = client.connect()
    print(f"connection {slave_address}: {connection}")

    # Send request to device and wait return
    response = client.read_holding_registers(register_address,num_registers,slave_address)
    
    # Check error
    if not response.isError():
        list_data = response.registers
        print(list_data)
        time.sleep(1)
    elif i<3:
        print("Error reading registers:", response)
        client.close()
        time.sleep(3)
        i = i+1
        list_data = read_sensor_rtu(register_address,num_registers,slave_address,i)
    else:
        if num_registers == 0x01:
            time.sleep(1)
            list_data = [0]
            print(list_data)
        else:
            time.sleep(1)
            list_data = [0,0]
            print(list_data)
            
    client.close()
    
    return list_data