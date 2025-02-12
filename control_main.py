import time
import datetime
import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

import read_water_level as level  
# import read_wd5 as wd5
import control_extra as extra


# Function controll fill full water tank  
def water_full(client, lv):
  if lv == 1:
    extra.valve_4(client, 1)
    time.sleep(35)
  while(level.water_tank(2) != 3):
    extra.valve_4(client, 1)
    time.sleep(5)
  extra.valve_4(client, 0)
   
# Function control irrigate plants  
def irrigate_plants(client,vol):
  # Calculate irrigation duration
  vol_need = 65 - vol
  if vol_need < 24:
    t = extra.calc_time(vol_need)
  else:
    t = 580
  # On Valve 3 and Pump 2 
  extra.valve_3(client, 1)
  extra.pump_2(client, 1)
  time.sleep(t+3)
  # Off Valve 3 and Pump 2 
  extra.pump_2(client, 0)
  extra.valve_3(client, 0)

# Function to fill irrigation tank
def irrigation_full(client):
  timeout = 0
  T_start = time.time()
  # Add nutrients to the irrigation tank
  extra.valve_2(client, 1)
  extra.pump_1(client, 1)
  time.sleep(4)
  extra.valve_2(client, 0)
  
  # Add water to the irrigation tank
  time.sleep(0.5)
  extra.valve_1(client, 1)
  
  
  while((level.irrigation_tank() != 3) and (timeout < 300) ):       # and (level.nutrient_tank() == 2)
    time.sleep(5)
    timeout = time.time() - T_start

  extra.valve_1(client, 0)
  extra.pump_1(client, 0)
  if level.nutrient_tank() == 1:
    print("Cảnh báo hết chất dinh dưỡng, hãy pha thêm vào thùng")
    return "Warning"
  else: 
    return "Ok"
  
# Function control irrigate system
def main(vol):
  client = extra.connect_relay()
  
  # Check level water in irrigation tank
  lv_irrigate = level.irrigation_tank()
  
  if lv_irrigate == 1:
    lv_water = level.water_tank(1)
    lv_nutrient = level.nutrient_tank()
    # Check level water in water tank
    if not lv_water == 3:
      water_full(client, lv_water)
      
    if lv_nutrient == 2:
      irrigation_full(client)
    elif lv_nutrient == 1:
      print("Cảnh báo hết chất dinh dưỡng, hãy pha thêm vào thùng")
      return "Warning"
      
    status = irrigate_plants(client,vol)
    
  elif lv_irrigate == 2 or lv_irrigate == 3:
    status = irrigate_plants(client,vol)
    
  return status
  
def mist(status, num):
  client = extra.connect_relay()
  
  if num == 1:
    # Check pump_3's status
    if status == "on":
      extra.pump_3(client, 0)
      time.sleep(60)
      # Check level water in water tank (case 3)
      lv_water = level.water_tank(3)
      if lv_water == 1:
        water_full(client, lv_water)
      extra.pump_3(client, 1)
    elif status == "off":
      # Check level water in water tank (case 1)
      lv_water = level.water_tank(1)
      if lv_water != 3:
        water_full(client, lv_water)
    extra.pump_3(client, 1)
    return "on"
  elif num == 2:
    extra.pump_3(client, 0)
    return "off"