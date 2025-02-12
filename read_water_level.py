# import subprocess
import os
import time
import pymodbus.client as ModbusClient

import control_extra as extra

def uno220gpio():
    command = "uno220gpio --status"
    
    # Open the RasPi terminal, run the uno220 command and retrieve the printed GPIO status data
    # process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True) 
    # output, error = process.communicate()
    output = os.popen(command).read()
    
    # if process.returncode == 0:
        # output_lines = output.decode().split('\n')  # Convert data to list lines
    output_lines = output.split('\n')
        
        # Find the line containing "value"
    value_index = None
    for idx, line in enumerate(output_lines):
        if "value" in line:
            value_index = idx
            break
        
    if value_index is not None:
        value_line = output_lines[value_index]  # Get the line containing the word "value"
        value_columns = value_line.split()      # Split it into columns
        values = value_columns[2:6]             # Retrieve the value from the 'value' column
        
    return values

def check():
    values = uno220gpio()
    
    for i in range(0,4): 
        if values[i]=='X':                          # Check GPIO Ports were enabled
            # subprocess.run(["lxterminal", "-e", "uno220gpio --export=all"])
            os.system("uno220gpio --export=all")
            time.sleep(3)
            values = uno220gpio()
    return values

def water_tank(i):
    values = check()
    # print("Value =",values[0])
    if values[0] == '1' :                           # Buoy 1 reply 1 <=> water level 2
        return 2
        
    elif values[0] == '0' :                         # Buoy 1 reply 0 <=> water level 1 or 3
        # print("Bắt đầu kiểm tra")
        if i == 1 :                                 # Case 1: When the water level in the tank is stable
            client=extra.connect_relay()
            extra.valve_4(client,1)
            time.sleep(35)                          # The time to pump water from level 1 to level 2 is 35 seconds
            extra.valve_4(client,0)
            client.close()
            
            values = check()
            if values[0] == '0':                    # Buoy 1 reply 0 <=> water level 3
                return 3
            elif values[0] == '1':                  # Buoy 1 reply 1 <=> water level 2
                return 2
        elif i == 2 :                               # Case 2: When the water level in the tank is rising
            return 3
        
        elif i == 3:                                # Case 3: When the water level in the tank is decreasing
            return 1
        
def nutrient_tank():
    values = check()
    if values[1]=='1':                        # Buoy 2 reply 1 <=> water level 1 (low)
            return 1
    elif values[1]=='0':                      # Buoy 2 reply 0 <=> water level 2 (high)
        return 2
    
def irrigation_tank():
    values = check()
    if values[2]=='0':                        # Buoy 3 reply 0 <=> water level 3 (full)  
        return 3
    elif values[2]=='1' and values[3]=='0':     # Buoy 3 reply 1 and buoy 4 reply 0 <=> water level 2 (mid)
        return 2
    elif values[3]=='1':                      # Buoy 4 reply 1 <=> water level 1 (low)
        return 1