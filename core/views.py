from django.shortcuts import render
from events.models import Event
from clubs.models import Club
from django.db.models import Q
# Create your views here.
def home(request):
    Events= Event.objects.all().order_by('-date')[:3]
    return render(request, 'home.html', {'events': Events})

def search(request):
    query = request.GET.get('q', '')  # get the search term
    clubs = Club.objects.none()
    events = Event.objects.none()

    if query:
        clubs = Club.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        events = Event.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'query': query,
        'clubs': clubs,
        'events': events
    }
    return render(request, 'search_results.html', context)