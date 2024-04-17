
from django.urls import path, include 
from rest_framework import routers, serializers, viewsets
from .viewsets import *
        
 
router = routers.DefaultRouter()
router.register(r'sensors_data', SensorsData_Viewsets)

urlpatterns = [
    path(r'api/',include(router.urls)),
]