from django.db import models

# Create your models here.
class StandardData(models.Model):
    min_soil_moisture = models.FloatField()
    max_soil_moisture = models.FloatField()
    min_ec = models.FloatField()
    max_ec = models.FloatField()
    fertilizer_ratio = models.FloatField()
    min_humidity = models.FloatField()
    max_temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "standard_data"    # Table name in the database
        get_latest_by = "created_at"

    def __str__(self):
        return f"StandardData at {self.created_at}"