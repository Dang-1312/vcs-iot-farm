import time
import datetime
import pymodbus.client as ModbusClient
from pymodbus.transaction import ModbusRtuFramer

import read_water_level as level  
import read_wd5 as wd5
import control_extra as extra


# Function controll fill full water tank  
def water_full(client):
  while(level.water_tank() == 2):
    extra.valve_4(client, 1)
    time.sleep(5)
  extra.valve_4(client, 0)
   
# Function control irrigate plants  
def irrigate_plants(client,vol):
  # Calculate irrigation duration
  t = extra.calc_time(60-vol)
  # On Valve 3 and Pump 2 
  extra.valve_3(client, 1)
  extra.pump_2(client, 1)
  time.sleep(t+10)
  # Off Valve 3 and Pump 2 
  extra.pump_2(client, 0)
  extra.valve_3(client, 0)

# Function to fill irrigation tank
def irrigation_full(client):
  while(level.irrigation_tank() != 3):
    extra.valve_1(client, 1)
    extra.pump_1(client, 1)
    time.sleep(5)
  extra.valve_1(client, 0)
  extra.pump_1(client, 0)

# Function control irrigate system
def main():
  client = extra.connect_relay()
  lv_irrigate = level.irrigation_tank()
  if not lv_irrigate == 3:
    lv_water = level.water_tank()
    if not lv_water == 3:
      water_full(client)
    irrigation_full(client)

  vol = float(wd5.main_read(1)[0])
  while (vol<60):
      irrigate_plants(client,vol)
      time.sleep(20)
      vol = wd5.main_read(1)[0]