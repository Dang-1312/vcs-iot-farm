####################################################################
######## Phase 1 used only autowartering for growing plant #########
####################################################################

Bảng channel relay và địa chỉ tương ứng với các thiết bị:
Channel	|Relay address	|Device
------------------------------------------------
CH1	|0x00		| Van 1 (thùng nước -> thùng tưới)
------------------------------------------------
CH2	|0x01		| Van 2 (thùng dinh dưỡng -> thùng tưới)
------------------------------------------------
CH3	|0x02		| Máy bơm hóa chất (Pump_1)
------------------------------------------------
CH4	|0x03		| Máy bơm tưới và Máy bơm chìm (trộn trong thùng tưới) (Pump_2)
------------------------------------------------
CH5	|0x04		| Máy bơm phun sương (Pump_3)
------------------------------------------------
CH6	|0x05		| Van 4 (vòi nước sinh hoạt -> thùng nước)
------------------------------------------------
CH7	|0x06		| Van 3 (thùng tưới -> máy bơm tưới) 
------------------------------------------------
CH8	|0x07		| Cấp nguồn cho 3 sensors Rika (reset_sensor)

List địa chỉ của 3 cảm biến RS485:
Slave_address	|Device
-------------------------------------
0x01		|CO2
-------------------------------------
0x02		|Humidity Temperature 
-------------------------------------
0x03		|pH

Thể tích đất trong thùng xốp trồng cây ~90lít

############ Một số thông số cần kiểm tra lại ###############
Thời gian để bơm đầy thùng trộn 50 lít (từ đáy thùng (mức 1) đến đầy thùng (mức 3))
Đo lượng nước máy bơm tưới bơm ra các béc trong một khoảng thời gian