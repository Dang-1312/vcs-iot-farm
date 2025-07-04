from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import SensorData, NutrientAlert
from .serializers import SensorDataSerializer, NutrientAlertSerializer
from django.shortcuts import render
from users.decorators import login_required_custom

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
@login_required_custom
def DashboardView(request):
    now = timezone.now()
    twelve_hours_ago = now - timedelta(hours=12)    # Get the time 12 hours ago

    latest_data = SensorData.objects.filter(timestamp__gte=twelve_hours_ago).order_by('timestamp') # Get data from the last 12 hours

    context = {
        'data': latest_data,
    }
    return render(request, 'sensor_data/dashboard.html', context)


# Nutrient alert view
class NutrientAlertAPIView(APIView):
    def post(self, request):
        serializer = NutrientAlertSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data.get('error_message')
            timestamp = serializer.validated_data.get('timestamp')
            if message == "Warning":
                serializer.save()
                return Response({"message": "Warning saved."}, status=status.HTTP_201_CREATED)

        elif message == "Success":
            latest_record = NutrientAlert.objects.first()  # vì ordering = ['-timestamp']
            if latest_record and latest_record.error_message == "Warning":
                serializer.save()
                return Response({"message": "Success saved after Warning."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "No need to save Success."}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid error_message value."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)