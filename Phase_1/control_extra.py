import time
import random
import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

import read_wd5 as wd5


# Function reset source for RS485 sensors       
def reset_sensor():
    client = extra.connect_relay()
    time.sleep(3)
    extra.reset_sensor(client, 1)
    time.sleep(60)
    extra.reset_sensor(client, 0)
    client.close()
    time.sleep(180)
    
# Calculate irriagation water volume and EC
def calc_ec(ec_s, mois_s, mois1, mois2, ec1, ec2):
    ec_i = (ec1 + ec2) / 2
    mois_i = (mois1 + mois2) / 2
    vol = (mois_i - mois_s)/100 * 90           
    ec_t = (ec_i - ec_s)/vol + ec_s
    return {ec_t, vol}

# Calculate irrigation duration
def calc_time(vol_need):
    vol_1s = 0.01                               # Giả sử máy bơm tưới bơm ra 0,01lít trong 1 giây
    t = vol_need/vol_1s
    return t

# Connect to Relay Ethernet
def connect_relay():
    client = ModbusClient.ModbusTcpClient(host= "192.168.1.204" , 
                                          port= 12345, 
                                          framer= ModbusRtuFramer,
                                          baudrate=9600,
                                          bytesize=8,
                                          parity="N",
                                          stopbits=1,
                                          errorcheck="crc",
                                          )
    
    connection = client.connect()
    return client

# Control Valve 1
def valve_1(client, sw):
    if sw==0:
        response = client.write_coil(address=0x00, value=0x00, slave=0x01)
        print(response)
    elif sw==1:
        response = client.write_coil(address=0x00, value=0xFF, slave=0x01)
        print(response)

# Control Valve 2        
def valve_2(client, sw):
    if sw==0:
        response = client.write_coil(address=0x01, value=0x00, slave=0x01)
        print(response)
    elif sw==1:
        response = client.write_coil(address=0x01, value=0xFF, slave=0x01)
        print(response)

# Control Valve 3        
def valve_3(client, sw):
    if sw==0:
        response = client.write_coil(address=0x06, value=0x00, slave=0x01)
        print(response)
    elif sw==1:
        response = client.write_coil(address=0x06, value=0xFF, slave=0x01)
        print(response)

# Control Valve 4        
def valve_4(client, sw):
    if sw==0:
        response = client.write_coil(address=0x05, value=0x00, slave=0x01)
        print(response)
    elif sw==1:
        response = client.write_coil(address=0x05, value=0xFF, slave=0x01)
        print(response)

# Control Pump 1        
def pump_1(client, sw):
    if sw==0:
        response = client.write_coil(address=0x02, value=0x00, slave=0x01)
        print(response)
    elif sw==1:
        response = client.write_coil(address=0x02, value=0xFF, slave=0x01)
        print(response)

# Control Pump 2        
def pump_2(client, sw):
    if sw==0:
        response = client.write_coil(address=0x03, value=0x00, slave=0x01)
        print(response)
    elif sw==1:
        response = client.write_coil(address=0x03, value=0xFF, slave=0x01)
        print(response)
      
# Control Pump 3  
def pump_3(client, sw):
    if sw==0:
        response = client.write_coil(address=0x04, value=0x00, slave=0x01)
        print(response)
    elif sw==1:
        response = client.write_coil(address=0x04, value=0xFF, slave=0x01)
        print(response)
        
# Control Pump 4
def reset_sensor(client, sw):
    if sw==0:
        response = client.write_coil(address=0x07, value=0x00, slave=0x01)
        print(response)
    elif sw==1:
        response = client.write_coil(address=0x07, value=0xFF, slave=0x01)
        print(response)