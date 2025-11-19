from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from events.models import Event
from clubs.models import Club
from django.db.models import Q
User= get_user_model()
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

@login_required
@user_passes_test(lambda u: u.is_superuser)  # only superuser can give staff permission
def user_list(request):
    users = User.objects.all().order_by("username")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = get_object_or_404(User, id=user_id)

        action = request.POST.get("action")

        if action == "make":
            user.is_staff = True
            user.save()
            messages.success(request, f"{user.username} is now staff.")
        elif action == "remove":
            user.is_staff = False
            user.save()
            messages.info(request, f"{user.username} is no longer staff.")

        return redirect("user-list")

    return render(request, "users/user_list.html", {"users": users})