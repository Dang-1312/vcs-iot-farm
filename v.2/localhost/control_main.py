import time
import datetime
import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

import read_water_level as level  
import read_wd5 as wd5
import control_extra as extra


# Adjust irrigation tank solution
def irrigation(client, ec_need):
  level = level.irrigation_tank()
  if level == 3 :
    return "Full"
  elif level == 2 or level == 1:
    start = time.time()
    
    adjust = 1
    while(adjust==1):
      ec_tank = wd5.main_read(2)
      current = time.time()
      if (current - start) >= 600:       # Giả sử thời gian để bơm từ đáy đến đầy thùng là 10phút
        adjust=0
        extra.valve_2(client, 0)
        time.sleep(0.5)
        extra.pump_1(client, 0)
        return "ERROR"
      
      if ec_tank == ec_need :
        adjust=0
        
      elif ec_tank < ec_need :
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
    return "OK"
  
def water_full():
  client = extra.connect_relay()
  while(level.water_tank() == 2):
    extra.valve_4(client, 1)
    time.sleep(5)
  extra.valve_4(client, 0)
  client.close()
     
def irrigate_plants(client, vol_need):
  extra.pump_2(client, 1)
  t = extra.calc_time(vol_need)
  time.sleep(t)
  extra.pump_2(client, 0)
  return "OK"

def main(ec_s, mois_s, mois1, mois2, ec1, ec2):
  if level.water_tank() == 2:
    water_full()
  
  client = extra.connect_relay()
  
  if level.nutrient_tank == 1:
    irrigate_plants(client, vol_need)
    client.close()
    return "HELP_2"
  
  else:
    ec_need = extra.calc_ec(ec_s, mois_s, mois1, mois2, ec1, ec2)[0]
    vol_need = extra.cacl_ec(ec_s, mois_s, mois1, mois2, ec1, ec2)[1]
    status = irrigation(client, ec_need)
    
    if status == "OK" :
      status == irrigate_plants(client, vol_need)
      client.close()
      return status
    
    elif status == "ERROR" :
      client.close()
      return status
  