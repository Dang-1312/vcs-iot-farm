from rest_framework import serializers
from project_app.models import SensorsData

class SensorsDataSerialiser(serializers.HyperlinkedModelSerializer):
     class Meta:
                 model = SensorsData
                 fields = ('id', 'Temp_air', 'Hum_air', 'CO2', 'pH' , 'Moisture_soil' , 'EC' , 'Temperature_soil' , 'Created_time', 'Updated_time')
