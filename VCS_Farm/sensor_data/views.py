from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData
from .serializers import SensorDataSerializer
from django.shortcuts import render

# Create your views here.
class SensorDataAPIView(APIView):
    def post(self, request):
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Data saved successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response({"message": "GET request received successfully!"}, status=status.HTTP_200_OK)

# User dashboard view
def DashboardView(request):
    latest_data = SensorData.objects.order_by('-timestamp')[:144][::-1]  # Retrieve the latest 144 records

    context = {
        'data': latest_data,
    }
    return render(request, 'sensor_data/dashboard.html', context)