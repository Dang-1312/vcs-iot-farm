from rest_framework import serializers
from .models import SensorData, NutrientAlert

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = '__all__'

class NutrientAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutrientAlert
        fields = '__all__'