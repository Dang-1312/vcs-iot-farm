import time
import random

import read_wd5 as wd5

"""
ec1: soil EC was measured;
ec2: watering tank EC was measured;
moisture: soil moisture was measured;
ec_c: soil EC we need;
mois_c: soil moisture we need
"""


# Calculate EC of watering tank required
def calculate_ec(case, a, b, c, d, moisture, ec1, ec_c, mois_c):
    if case==1 :
        i1 = ec1 * moisture/100 * 85                        # Lượng chất tan trong đất
        w = (d - moisture)/100 * 85                         # Lượng nước trong thùng tưới vs thể tích đất khô là 85cm3
        i2 = b * (moisture/100 * 85 + w)  - i1              # Lượng chất tan trong dung dịch tưới 
        ec2 = i2/w - (random.randint(1,3) / 10)
        return ec2
    elif case==2 :
        i1 = ec1 * moisture/100 * 85                       
        w = (mois_c - moisture)/100 * 85                        
        i2 = ec_c * (moisture/100 * 85 + w)  - i1          
        ec2 = i2/w
        return ec2
    elif case==3 :
        i1 = ec1 * moisture/100 * 85                       
        w = (mois_c - moisture)/100 * 85                        
        i2 = ec_c * (moisture/100 * 85 + w)  - i1          
        ec2 = i2/w
        return ec2
    
    
def main_cal (m1, M1, ec_c, m2, M2, mois_c):
    soil_data = wd5.main_read(1)
    ec_1 = soil_data[1]
    moisture = soil_data[0]    
    
    time.sleep(1)
    
    ec_2 = wd5.main_read(2)[1]
    
    # Case 0 all right
    if (m1 < ec_1 < M1) and (m2 < moisture < M2) :
        return 0
    # Case 1 soil EC is wrong and soil moisture is right
    elif (m2 < moisture < M2) :
        ec3 = calculate_ec(case=1, d=M2, moisture=moisture, ec1=ec_1, ec_c=ec_c)
        return ec3
    # Case 2 soil EC is right and soil moisture is wrong
    elif (m1 < ec_1 < M1) :
        ec3 = calculate_ec(case=2, b=M1, moisture=moisture, ec1=ec_1, ec2=ec_2)
        return ec3
    # Case 3 all wrong
    else:
        ec3 = calculate_ec(case=3, moisture=moisture, ec1=ec_1, ec2=ec_2, ec_c=ec_c, mois_c=mois_c)
        return ec3
        
    
    