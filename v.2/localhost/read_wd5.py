import serial
import time
import datetime
import sys

from pytz import timezone


def now_utc_str():
    return datetime.datetime.now(timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S") 

def product_to_number(product):
    if product == "5WT":
        return 2
    elif product == "5WET":
        return 3
    elif product == "5WTA":
        return 5
    else:
        return 0

def main_read(i):
    if i==1:
        portName = "/dev/ttyUSB0"
    elif i==2:
        portName= "/dev/ttyUSB0"
    waitTime = 0.5

    address = 0
    type = 0
    length = 0
    check = 0

    # Connect to device
    sdi = serial.Serial(
                port = portName,
                baudrate = 1200,
                bytesize = serial.SEVENBITS,
                parity = serial.PARITY_EVEN,
                stopbits = serial.STOPBITS_ONE,
                timeout = 0,
                write_timeout = 0)

    sdi.reset_input_buffer()
    sdi.reset_output_buffer()

    time.sleep(0.5)

    # Loop send identification
    while length != 34:
        try:
            sdi.reset_input_buffer()
            sdi.reset_output_buffer()
            
            #Break Send
            sdi.break_condition = True
            time.sleep(0.012)
            sdi.break_condition = False
            time.sleep(0.00833)
            
            request = str(address) + "I!"
            sdi.write( request.encode() )
            print(request)
            time.sleep(waitTime)
            
            # Write Check
            response = sdi.readline()
            print(response)
            
            # Parse
            length = len(response)
            if length == 34:
                sdi_ver = response[5:7].decode('Shift_JIS')
                company = response[7:15].decode('Shift_JIS').strip()
                product = response[15:21].decode('Shift_JIS').strip()
                version = response[21:24].decode('Shift_JIS')
                option  = response[24:length-2].decode('Shift_JIS').strip()
                print("sdi_ver:" + sdi_ver)
                print("company:" + company)
                print("product:" + product)
                print("version:" + version)
                print("option :" + option)
                if response[4:5].decode('Shift_JIS') != str(address):
                    address = address + 1
                    continue
                if sdi_ver != "13":
                    address = address + 1
                    continue
                address_right = address
                type_product = product_to_number(product)
                now = now_utc_str()
            else:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Measurement has been cancelled.")
            break
    
    # Loop Measurement
    while check == 0:    
        try:
            sdi.reset_input_buffer()
            sdi.reset_output_buffer()
            
            #Break Send
            sdi.break_condition = True
            time.sleep(0.012)
            sdi.break_condition = False
            time.sleep(0.00833)
            
            request = str(address) + "M!"
            sdi.write( request.encode() )
            print("measure request ",request)
            time.sleep(waitTime)
            
            #Write Check
            response = sdi.readline()
            print("measure response ", response)
            response = response.rstrip()
            
            # Start measurement
            # <BR>0M!00013<CR><LF>
            resAddress = response[4:5].decode('Shift_JIS')
            resInterval = response[5:8].decode('Shift_JIS')
            resItemCount = response[8:9].decode('Shift_JIS')
            
            if str(address) == resAddress and str(type_product) == resItemCount:
                    time.sleep(int(resInterval))
                
                    # Receive response 0<CR><LF>
                    dummyRead = sdi.readline()
                    sdi.reset_input_buffer()
                    sdi.reset_output_buffer()
                    
                    #Break Send
                    sdi.break_condition = True
                    time.sleep(0.012)
                    sdi.break_condition = False
                    time.sleep(0.00833)
                    
                    request = str(address) + "D0!"
                    sdi.write(request.encode())     # Send 0D0!
                    time.sleep(waitTime)
                    measured = sdi.readline()
                    print("Send measurement data:",measured," ;",len(measured))
                    if len(measured)==22 or len(measured)==23:
                        d = datetime.datetime.now()
                        dt = d.strftime('%Y/%m/%d %H:%M:%S')
                        
                        if measured[1:6].decode('Shift_JIS') == str(address) + "D0!"+ str(address):
                            # Loai bo cac phan header va footer chi giu lai phan noi dung chinh
                            measured = measured.rstrip().decode('Shift_JIS')        
                            replaced = measured.replace('+',',')
                            replaced = replaced.replace('-',',-')
                            # Dua tu dang string thanh dang list
                            data = replaced.split(',')
                            now = now_utc_str()
                            if len(data) == 3:
                                print("Volume Water Content:" + data[1])
                                print("Temperature         :" + data[2])
                            elif len(data) == 4:
                                print("Volume Water Content:" + data[1])
                                print("EC                  :" + data[2])
                                print("Temperature         :" + data[3])
                            elif len(data) == 6:
                                print("Volume Water Content:" + data[1])
                                print("Temperature         :" + data[2])
                                print("X-axis              :" + data[3])
                                print("Y-axis              :" + data[4])
                                print("Z-axis              :" + data[5])
                            print("Time         :" + now)
                            print("Done")
                            check = 1
                        else:
                            check = 0
                    else:
                        print("Response invalid")
                        d = datetime.datetime.now()
                        dt = d.strftime('%Y/%m/%d %H:%M:%S')
                        print(dt)
                        check = 0
            # else:
            #     check = 0
            time.sleep(1)
        except KeyboardInterrupt:
            print("Measurement has been cancelled.")
            break
        except Exception as error:
            # handle the exception              
            print("An error occurred:", type(error).__name__, "–", error) 
    
    # Close connect and return data
    sdi.close()
    return [data[1] , data[2] , data[3]]