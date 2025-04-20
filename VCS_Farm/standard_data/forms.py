from django import forms
from .models import StandardData

class StandardDataForm(forms.ModelForm):
    class Meta:
        model = StandardData
        fields = [
            'min_soil_moisture', 'max_soil_moisture',
            'min_ec', 'max_ec',
            'fertilizer_ratio',
            'min_humidity', 'max_temperature'
        ]
        widgets = {
            field: forms.NumberInput(attrs={'class': 'form-control'})
            for field in fields
        }
