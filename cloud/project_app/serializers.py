from rest_framework import serializers

# import models
from project_app.models import *

class SensorsData_Serializer(serializers.ModelSerializer):
    class Meta:
        model = SensorsData
        fields = '__all__'