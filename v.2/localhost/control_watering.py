import time
import datetime
import pymodbus.client as ModbusClient

from pymodbus.transaction import ModbusRtuFramer

# Import my code
import read_water_level as level  
import read_wd5 as wd5
import control_calculate as calc

def on_system(status, ec, vol, vol1, vol2, ec1, ec2):
  level_3 = level.water_tank(old=3, v4=0)
  if not level_3 == 3:
    ec_n = calc.cal_ec(ec, vol, vol1, vol2, ec1, ec2)