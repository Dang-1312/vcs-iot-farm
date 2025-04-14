import time
import datetime
import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

import read_level as level  
import extra


# Function controll fill full water tank  
def water_full(client, lv):
  if lv == 1:
    extra.valve_4(client, 1)
    time.sleep(15)
  while(level.water_tank(2) != 3):
    extra.valve_4(client, 1)
    time.sleep(5)
  extra.valve_4(client, 0)

# Function to fill irrigation tank
def irrigation_full(client):
  timeout = 0
  T_start = time.time()
  # Add nutrients to the irrigation tank
  extra.valve_2(client, 1)
  extra.pump_1(client, 1)
  time.sleep(5)
  extra.valve_2(client, 0) 
  # Add water to the irrigation tank
  time.sleep(0.5)
  extra.valve_1(client, 1) 
  # Loop check level and error
  while ((level.irrigation_tank() != 3) and (timeout < 300)):       # and (level.nutrient_tank() == 2)
    time.sleep(5)
    timeout = time.time() - T_start
  extra.valve_1(client, 0)
  extra.pump_1(client, 0)
  # Check remaining nutrient levels
  if level.nutrient_tank() == 1:
    # print("Cảnh báo hết chất dinh dưỡng, hãy pha thêm vào thùng")
    return "Warning"
  else: 
    return "Success"

# Function control irrigate plants  
def irrigate_plants(client,vol_need):
  status = "Success"
  # Calculate irrigation duration
  t = extra.calc_time(vol_need)
  # On Valve 3 and Pump 2 
  extra.valve_3(client, 1)
  extra.pump_2(client, 1)
  # Loop irrigation
  while (t > 0):
    time.sleep(3)
    t = t - 3
    if level.irrigation_tank() == 1:
      extra.valve_3(client,0)
      extra.pump_2(client,0)
      status = irrigation_full(client)
      extra.valve_3(client, 1)
      extra.pump_2(client, 1)
  # Off Valve 3 and Pump 2 
  extra.pump_2(client, 0)
  extra.valve_3(client, 0)
  return status

# Function control irrigate system
def irrigate(vol):
  client = extra.connect_relay()
  # Check level water in irrigation tank
  lv_irrigate = level.irrigation_tank()
  # Add nutrient solution to the irrigation tank if at level 1
  if lv_irrigate == 1:
    lv_water = level.water_tank(1)
    lv_nutrient = level.nutrient_tank()
    # Check level water in water tank
    if not lv_water == 3: 
      water_full(client, lv_water)
    status = irrigation_full(client)
    if status == "Warning":
      irrigate_plants(client,vol)             
    else:
      status = irrigate_plants(client,vol)
  # Irrigate if solution above level 1
  elif lv_irrigate == 2 or lv_irrigate == 3:
    status = irrigate_plants(client,vol)
  # Return status after irrigation
  return status
  
def mist(status):
  client = extra.connect_relay()
  # Check status
  if status == 0:
    lv_water = level.water_tank(1)
    if lv_water != 3:
      water_full(client)
  elif status>0:
    lv_water = level.water_tank(3)
    if lv_water == 1:
      water_full(client)
  extra.pump_3(client,1)
  time.sleep(600)
  extra.pump_3(client,0)
  return status + 1