from django.urls import path
from .views import SensorDataAPIView, DashboardView, NutrientAlertAPIView

urlpatterns = [
    path('api/sensor_data/', SensorDataAPIView.as_view(), name='sensor_data_api'),
    path('dashboard/', DashboardView, name='dashboard'),
    path('api/report_error/', NutrientAlertAPIView.as_view(), name='report_error'),
]