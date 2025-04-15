from django.db import models

# Create your models here.
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