from rest_framework import viewsets
from project_app.serializers import *

class SensorsData_Viewsets(viewsets.ModelViewSet):
    queryset = SensorsData.objects.all()
    serializer_class = SensorsData_Serializer