# Workflow D:\VCS\Cơ sở lập trình\auto_watering.drawio
import time
import datetime
import pymodbus.client as ModbusClient

from pymodbus.transaction import ModbusRtuFramer

import read_water_level as level    
# 0 có thể hiểu là tắt và 1 có thể hiểu là bật

now=datetime.datetime.now()
    
def check_on():
    now=datetime.datetime.now()
    h=now.hour
    m=now.minute
    if (h==8 and 0<=m<=10) or (h==16 and 0<=m<=10):
        return 1
    else:
        return 0

def check_off(h_off,m_off):
    now=datetime.datetime.now()
    h=now.hour
    m=now.minute
    if h==h_off and m>=m_off:
        return 0
    else:
        return 1
    
def watering(so,h_off,m_off):           # so: Trạng thái hệ thống bơm hiện tại (0 là đang tắt, 1 là đang bật)
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
    print(f"connection: {connection}")
    
    # Hiện tại đang tắt cần kiểm tra điều kiện bật hệ thống bơm
    if so==0:               
        sn = check_on()     # sn: Status new
        if sn==1:   
            if level.water_level(3,1,1)==1:        
                response = client.write_coil(address=0x05, value=0xFF, slave=0x01)        # Mở van 4
                print(response)
                time.sleep(10)
                
                response = client.write_coil(address=0x00, value=0xFF, slave=0x01)        # Mở van 1
                print(response)
                time.sleep(0.5)
                
                response = client.write_coil(address=0x02, value=0xFF, slave=0x01)        # Mở bơm hóa chất
                print(response)
                time.sleep(0.5)
            
            response = client.write_coil(address=0x06, value=0xFF, slave=0x01)        # Mở van 3
            print(response)
            time.sleep(0.5)
            
            response = client.write_coil(address=0x03, value=0xFF, slave=0x01)        # Mở bơm tưới
            print(response)
            time.sleep(0.5)
            
            client.close()
            return [1, now.hour(), now.minute()+10]
        
        else:
            client.close()
            return [0,0,0]
    # Hiện tại đang bật cần kiểm tra điều kiện tắt hệ thống bơm
    elif so==1:
        sn=check_off(h_off,m_off)
        if level.water_level(3,1,1)==3:
            response = client.write_coil(address=0x05, value=0x00, slave=0x01)        # Tắt van 4
            print(response)
            
            response = client.write_coil(address=0x02, value=0x00, slave=0x01)        # Tắt bơm hóa chất
            print(response)
            
            response = client.write_coil(address=0x00, value=0x00, slave=0x01)        # Tắt van 1
            print(response)
            
        if sn==0 or level.water_level(3,1,1)==1:   
            response = client.write_coil(address=0x05, value=0x00, slave=0x01)        # Tắt van 4
            print(response)
            
            response = client.write_coil(address=0x02, value=0x00, slave=0x01)        # Tắt bơm hóa chất
            print(response)
            
            response = client.write_coil(address=0x00, value=0x00, slave=0x01)        # Tắt van 1
            print(response)
                  
            response = client.write_coil(address=0x03, value=0x00, slave=0x01)        # Tắt bơm tưới
            print(response)
            
            response = client.write_coil(address=0x06, value=0x00, slave=0x01)        # Tắt van 3
            print(response)
            
            client.close()
            return [0]
        
        else:
            return [1,h_off,m_off]