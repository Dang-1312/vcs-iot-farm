from django.contrib import admin
from projects.models import MoistureSensorData

# Register your models here.

@admin.register(MoistureSensorData)
class MoistureSensorData(admin.ModelAdmin):
    list_display = ["id", "Water_content", "EC", "Temperature", "Created_time", "Updated_time"]
    admin.register(MoistureSensorData)