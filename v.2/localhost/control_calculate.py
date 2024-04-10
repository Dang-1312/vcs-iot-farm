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
def cal_ec(ec, vol, vol1, vol2, ec1, ec2):
    ec_t = wd5.main_read(2)
    ec_c = (ec1 + ec2) / 2
    vol_c = (vol1 + vol2) / 2
    
    ec_n = 0
    return ec_n