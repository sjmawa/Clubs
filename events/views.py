from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.forms import EventForm
# Create your views here.
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            #return redirect('event-detail', event.id)  # adjust name to your event detail view
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EventForm()
    
    return render(request, 'events/create_event.html', {'form': form})