from django.shortcuts import render
from .models import Locations

def post_list(request):
    locations = Locations.objects.all()[1:10]
    return render(request, 'hgss/main.html', {'locations':locations})
