from django.http import JsonResponse
from project_app.models import SensorsData

def getJson(request):
    obj = SensorsData.objects.all()
    data = { "result" :list(obj.values('id', 'Temp_air', 'Hum_air', 'CO2', 'pH' , 'Moisture_soil' , 'EC' , 'Temperature_soil' , 'Created_time', 'Updated_time'))
            }
    return JsonResponse(data)
