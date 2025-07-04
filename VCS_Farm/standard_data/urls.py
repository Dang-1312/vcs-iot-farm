from django.urls import path
from .views import StandardView

urlpatterns = [
    path('standard_input/', StandardView, name='standard_input'),
]