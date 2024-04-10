Bảng channel relay và địa chỉ tương ứng với các thiết bị:
Channel	|Relay address	|Device
------------------------------------------------
CH1	|0x00		| Van 1 (thùng nước -> thùng tưới)
------------------------------------------------
CH2	|0x01		| Van 2 (thùng dinh dưỡng -> thùng tưới)
------------------------------------------------
CH3	|0x02		| Máy bơm hóa chất
------------------------------------------------
CH4	|0x03		| Máy bơm tưới
------------------------------------------------
CH5	|0x04		| Máy bơm phun sương
------------------------------------------------
CH6	|0x05		| Van 4 (vòi nước sinh hoạt -> thùng nước)
------------------------------------------------
CH7	|0x06		| Van 3 (thùng tưới -> máy bơm tưới)
------------------------------------------------
CH8	|0x07		| Máy bơm chìm (trộn trong thùng tưới)

List địa chỉ của 3 cảm biến RS485:
Slave_address	|Device
-------------------------------------
0x01		|CO2
-------------------------------------
0x02		|Humidity Temperature 
-------------------------------------
0x03		|pH

Payload gửi từ AWS IoT về có dạng {"Status": value,"EC": value,"Vol": value,"Vol_1": value,"Vol_2": value,"EC_1": value,"EC_2": value}
- Status: trạng thái hiện tại của hệ thống bơm
- EC và Vol: EC và độ ẩm đất lần đo gần nhất
- Vol_1 và Vol_2 : Khoảng độ ẩm đất phù hợp với từng giai đoạn phát triển Vol_1 <= Vol <= Vol_2
- EC_1 và EC_2 : Khoảng EC đất phù hợp với từng giai đoạn phát triển EC_1 <= EC <= EC_2