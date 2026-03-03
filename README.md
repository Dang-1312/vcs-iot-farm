# vcs-iot-farm

---

**Developer:** Dang Nguyen  
**Email:** minhdangnc@gmail.com  
*For any questions or support regarding this project, please contact the developer above.*

---

## Bảng channel relay và địa chỉ tương ứng với các thiết bị:
|Channel	|Relay address	|Device|
|:------|:--------------|:------------------------------------------------|
|CH1 	|0x00		    | Van 1 (thùng nước -> thùng tưới)|
|CH2	|0x01		    | Van 2 (thùng dinh dưỡng -> thùng tưới)|
|CH3 	|0x02		    | Máy bơm hóa chất (Pump_1)|
|CH4	|0x03		    | Máy bơm tưới và Máy bơm trộn (Pump_2 + Pump_4)|
|CH5 	|0x04		    | Máy bơm phun sương (Pump_3)|
|CH6	|0x05		    | Van 4 (vòi nước sinh hoạt -> thùng nước)|
|CH7	|0x06		    | Van 3 (thùng tưới -> máy bơm tưới)|
|CH8	|0x07		    | Công tắc nguồn 12V cho RS485 sensors|

## List địa chỉ của 3 cảm biến RS485:
|Slave_address	|Device              |
|:--------------|:-------------------|
|0x01		    |Soil 7in1           |
|0x02    		|CO2                 |
|0x03	    	|Humidity Temperature|

## Tổng quan về các apps trong Django project VCS_Farm:
|Tên app   |Trách nhiệm   |Table DB chính  |
|:------|:------------------------------------------------|:--------------|
|sensor_data   |Các chức năng liên quan việc nhập xuất dữ liệu của cảm biến   |SensorData   |
|standard_data  |Các chức năng liên quan việc nhập xuất dữ liệu tiêu chuẩn   |StandardData   |
|users   |Các chức năng liên quan việc thao tác với dữ liệu người dùng   |UserData   |
