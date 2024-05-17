# vcs-iot-farm
# Bảng channel relay và địa chỉ tương ứng với các thiết bị:
Channel	|Relay address	|Device
------------------------------------------------
CH1	    |0x00		    | Valve 1 (thùng nước -> thùng tưới)
------------------------------------------------
CH2	    |0x01		    | Valve 2 (thùng dinh dưỡng -> thùng tưới)
------------------------------------------------
CH3	    |0x02		    | Pump 1(Máy bơm hóa chất)
------------------------------------------------
CH4	    |0x03		    | Pump 2(Máy bơm tưới)
------------------------------------------------
CH5	    |0x04		    | Pump 3(Máy bơm phun sương)
------------------------------------------------
CH6	    |0x05		    | Valve 4 (vòi nước sinh hoạt -> thùng nước)
------------------------------------------------
CH7	    |0x06		    | Valve 3 (thùng tưới -> máy bơm tưới)
------------------------------------------------
CH8 	|0x07		    | Pump 4 (Máy bơm chìm trộn trong thùng tưới)

# List địa chỉ của 3 cảm biến RS485:
Slave_address	|Device
-------------------------------------
0x01		    |CO2
-------------------------------------
0x02	    	|Humidity Temperature 
-------------------------------------
0x03	    	|pH

# List Port GPIO ứng với các phao từ và thùng chứa
Port    |phao   |thùng
--------------------------
0       |phao 1 | nước
--------------------------
1       |phao 2 | dinh dưỡng
--------------------------
2       |phao 3 | thùng tưới
--------------------------
3       |phao 4 | thùng tưới

# Payload gửi từ AWS IoT về có dạng {"EC": value,"Mois": value,"Mois_1": value,"Mois_2": value,"EC_1": value,"EC_2": value}
- EC và Mois: EC và độ ẩm đất lần đo gần nhất
- Mois_1 và Mois_2 : Khoảng độ ẩm đất phù hợp với từng giai đoạn phát triển Vol_1 <= Vol <= Vol_2
- EC_1 và EC_2 : Khoảng EC đất phù hợp với từng giai đoạn phát triển EC_1 <= EC <= EC_2