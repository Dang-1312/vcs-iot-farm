from django.db import models

# Create your models here.
# Class to store sensors data
class SensorData(models.Model):
    soil_moisture = models.FloatField()
    soil_temperature = models.FloatField()
    ec = models.FloatField()
    soil_nitrogen = models.FloatField()
    soil_phosphorus = models.FloatField()
    soil_potassium = models.FloatField()
    ph = models.FloatField()
    co2 = models.FloatField()
    temp_air = models.FloatField()
    hum_air = models.FloatField()
    timestamp = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sensors_data"    # Table name in the database
        get_latest_by = "created_at"

    def __str__(self):
        return f"SensorData at {self.created_at}"
    
# Class notice when the nutrient is not enough
class NutrientAlert(models.Model):
    error_message = models.CharField(max_length=100)  # "Warning" hoặc "Success"
    timestamp = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "nutrient_alert"  # Table name in the database
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"{self.error_message} - {self.timestamp}"