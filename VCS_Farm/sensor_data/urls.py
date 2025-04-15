from django.urls import path
from .views import SensorDataAPIView

urlpatterns = [
    path('api/sensor_data/', SensorDataAPIView.as_view(), name='sensor_data_api'),
]