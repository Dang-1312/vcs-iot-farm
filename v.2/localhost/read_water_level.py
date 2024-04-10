import subprocess
import time

def uno220gpio():
    command = "uno220gpio --status"
    
    # Open terminal on RasPi and retrieve the printed data
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True) 
    output, error = process.communicate()
    
    if process.returncode == 0:
        output_lines = output.decode().split('\n')  # Convert data to list lines
        
        # Find the line containing "value"
        value_index = None
        for idx, line in enumerate(output_lines):
            if "value" in line:
                value_index = idx
                break
        
        if value_index is not None:
            value_line = output_lines[value_index]  # Retrieve the line containing "value"
            value_columns = value_line.split()      # Split it into columns
            values = value_columns[2:6]             # Retrieve the value from the 'value' column
    return values

def check():
    values = uno220gpio()
    
    for i in range(0,8): 
        if values[i]=='X':                          # Check GPIO Ports were enabled
            subprocess.run(["lxterminal", "-e", "uno220gpio --export=all"])
            time.sleep(3)
            values = uno220gpio()
    return values

def water_tank(old, v4):
    values = check()
    if values[0]=='1':                        # Buoy 1 reply 1 <=> water's level 2 (mid)
            return 2
    elif values[0]=='0':                      # Buoy 1 reply 0 (2 scenarios: full or low)
        if (old==2 or old==3) and v4==1 :   # The previous water level of the float is 2 or 3, and the electric valve is open to drain water into the tank => (full)
            return 3
        elif (old==2 and v4==0) or old==1:  # The previous water level of the float is 1 or (2 and the electric valve is close)  => (low)
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