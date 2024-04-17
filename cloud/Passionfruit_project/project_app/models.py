from time import timezone
from django.db import models

# Create your models here.
class SensorsData(models.Model):
    Created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    Temp_air = models.DecimalField(max_digits=3, decimal_places=2)
    Hum_air = models.DecimalField(max_digits=3, decimal_places=2)
    CO2 = models.IntegerField(max_length=4)
    pH = models.DecimalField(max_digits=2, decimal_places=2)
    Moisture_soil = models.DecimalField(max_digits=3, decimal_places=2)
    EC = models.DecimalField(max_digits=2, decimal_places=2)
    Temperature_soil = models.DecimalField(max_digits=3, decimal_places=2)
    Updated_time = models.DateTimeField(auto_now=True, auto_now_add=False)