import time
import datetime
import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

import read_water_level as level  
import read_wd5 as wd5
import control_extra as extra


# Function adjust irrigation tank solution
def irrigation(client, ec_need):
  level_tank = level.irrigation_tank()
  if level_tank == 3 :
    return "FULL"
  elif level_tank == 2 or level == 1:
    start = time.time()
    
    adjust = 1
    while(adjust==1):
      ec_tank = wd5.main_read(2)
      current = time.time()
      if (current - start) >= 600:       # Giả sử thời gian để bơm từ đáy đến đầy thùng là 10phút
        adjust=0
        extra.valve_1(client, 0)
        extra.valve_2(client, 0)
        time.sleep(0.5)
        extra.pump_1(client, 0)
        return "ERROR"
        
      if ec_tank < ec_need :
        extra.valve_2(client,1)
        time.sleep(0.5)
        extra.pump_1(client, 1)
        time.sleep(10)
        ec_tank = wd5.main_read(2)
        if level.irrigation_tank() == 3 or ec_tank > ec_need or level.nutrient_tank() == 1 :
          adjust=0
          extra.valve_2(client, 0)
          time.sleep(0.5)
          extra.pump_1(client, 0)
          if level.nutrient_tank() == 1:
            return "HELP"  
      elif ec_tank > ec_need :
        extra.valve_1(client,1)
        time.sleep(0.5)
        extra.pump_1(client, 1)
        time.sleep(10)
        ec_tank = wd5.main_read(2)
        if level.irrigation_tank() == 3 or ec_tank < ec_need or level.water_tank() == 1 :
          adjust=0
          extra.valve_1(client, 0)
          time.sleep(0.5)
          extra.pump_1(client, 0)  
      elif ec_tank == ec_need :
        adjust=0
        
    extra.pump_4(client, 1)
    time.sleep(60)
    return "OK"
 
# Function controll fill full water tank  
def water_full():
  client = extra.connect_relay()
  while(level.water_tank() == 2):
    extra.valve_4(client, 1)
    time.sleep(5)
  extra.valve_4(client, 0)
  client.close()
   
# Function control irrigate plants  
def irrigate_plants(client, vol_need):
  # Calculate irrigation duration
  t = extra.calc_time(vol_need)
  # On Valve 3 and Pump 2 
  extra.valve_3(client, 1)
  extra.pump_2(client, 1)
  time.sleep(t)
  # Off Valve 3 and Pump 2 
  extra.pump_2(client, 0)
  extra.valve_3(client, 0)
  extra.pump_4(client, 0)

# Function control irrigate system
def main(ec_s, mois_s, mois1, mois2, ec1, ec2):
  # Check liquid level in water tank
  if level.water_tank() == 2:
    water_full()
  
  # Connect to Relay Ethernet
  client = extra.connect_relay()
  
  # Check liquid level in nutrient tank
  if level.nutrient_tank == 1:
    vol_need = extra.cacl_ec(ec_s, mois_s, mois1, mois2, ec1, ec2)[1]
    irrigate_plants(client, vol_need)
    client.close()
    return "HELP"
  
  else:
    ec_need = extra.calc_ec(ec_s, mois_s, mois1, mois2, ec1, ec2)[0]
    vol_need = extra.cacl_ec(ec_s, mois_s, mois1, mois2, ec1, ec2)[1]
    
    # Adjust irrigation tank solution
    status = irrigation(client, ec_need)
    
    # Check status irrigate system and control irrigate plants
    if status == "OK" or status == "FULL":
      irrigate_plants(client, vol_need)
      client.close()
      return "OK"
    
    elif status == "HELP":
      irrigate_plants(client, vol_need)
      client.close()
      return status
    
    elif status == "ERROR" :
      client.close()
      return status
  