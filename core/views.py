from django.shortcuts import render
from events.models import Event
# Create your views here.
def home(request):
    Events= Event.objects.all().order_by('-date')[:3]
    return render(request, 'home.html', {'events': Events})