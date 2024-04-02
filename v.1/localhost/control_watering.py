# from awscrt import io, mqtt, auth, http
# from awsiot import mqtt_connection_builder

import pymodbus.client as ModbusClient

from pymodbus.transaction import ModbusRtuFramer

import time
import json

import read_water_level as lv
import read_wd5 as wd5
import control_calculate as cal 

# Connect to POE ETH Relay
client = ModbusClient.ModbusTcpClient(host= '192.168.1.204' , 
                                          port= 12345, 
                                          framer= ModbusRtuFramer,
                                          baudrate=9600,
                                          bytesize=8,
                                          parity="N",
                                          stopbits=1,
                                          errorcheck="crc",
                                          )
connection = client.connect()
print(f"connection: {connection}")


