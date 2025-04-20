from django.shortcuts import render, redirect
from .models import StandardData
from .forms import StandardDataForm

# Create your views here.
def StandardView(request):
    latest_record = StandardData.objects.latest('created_at')

    if request.method == 'POST':
        form = StandardDataForm(request.POST)       # Retrieve input data from the form template
        if form.is_valid():
            instance = form.save(commit=False)
            # Round the input data
            instance.min_soil_moisture = round(instance.min_soil_moisture, 1)
            instance.max_soil_moisture = round(instance.max_soil_moisture, 1)
            instance.min_ec = round(instance.min_ec, 1)
            instance.max_ec = round(instance.max_ec, 1)
            instance.fertilizer_ratio = round(instance.fertilizer_ratio, 1)
            instance.min_humidity = round(instance.min_humidity, 1)
            instance.max_temperature = round(instance.max_temperature, 1)
            # Save the data after rounding
            instance.save()
            return redirect('input')
    else:
        form = StandardDataForm()
    
    return render(request, 'standard_data/standard_input.html', {
        'form': form,
        'latest_record': latest_record
    })