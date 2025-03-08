# vcs-iot-farm
## Bảng channel relay và địa chỉ tương ứng với các thiết bị:
|Channel	|Relay address	|Device|
|:------|:-------------:|------------------------------------------------:|
|CH1 	|0x00		    | Van 1 (thùng nước -> thùng tưới)|
|CH2	|0x01		    | Van 2 (thùng dinh dưỡng -> thùng tưới)|
|CH3 	|0x02		    | Máy bơm hóa chất (Pump_1)|
|CH4	|0x03		    | Máy bơm tưới và Máy bơm trộn (Pump_2 + Pump_4)|
|CH5 	|0x04		    | Máy bơm phun sương (Pump_3)|
|CH6	|0x05		    | Van 4 (vòi nước sinh hoạt -> thùng nước)|
|CH7	|0x06		    | Van 3 (thùng tưới -> máy bơm tưới)|
|CH8	|0x07		    | Cấp nguồn 12V cho RS485 sensors|

## List địa chỉ của 3 cảm biến RS485:
|Slave_address	|Device              |
|:--------------|-------------------:|
|0x01		    |Soil 7in1           |
|0x02    		|CO2                 |
|0x03	    	|Humidity Temperature|

## Một số thông số khác
- Tỉ lệ phân bón trong thùng 2 **~210gram/30 lít** <=> EC **~7.5 mS/cm**
- Nồng độ EC trong thùng tưới nếu pha đúng tỉ lệ EC **~0.23 mS/cm**
- Tỉ lệ thời gian bơm thùng 2 / thùng 1 **~4/296 giây**
- Thể tích đất trong thùng xốp trồng cây **~ 90 lít**
- Máy bơm tưới bơm ra **~0,55 lít/béc/phút**
- Thời gian để bơm đầy thùng nước (từ mức 1 đến mức 3) **~351 giây**
- Thời gian để tưới hết nước trong thùng tưới ra **~592 giây/50 lít**
- Thời gian để bơm đầy thùng trộn 50 lít (từ đáy thùng (mức 1) đến đầy thùng (mức 3)) **~5 phút**
