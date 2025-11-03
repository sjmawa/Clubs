from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from clubs.models import Club, ClubRole, ClubMembership
from clubs.forms import ClubForm, ClubRoleForm
from django.utils import timezone

def club_list(request):
    clubs = Club.objects.all()
    return render(request, 'club_list.html', {'clubs': clubs})

def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    is_member = False

    if request.user.is_authenticated:
        is_member = club.memberships.filter(user=request.user).exists()
    members = ClubMembership.objects.filter(club=club)
    roles = ClubRole.objects.filter(club=club)
    return render(request, 'club_detail.html', {
        'club': club,
        'members': members,
        'roles': roles,
        'is_member': is_member
    })
@login_required(login_url='sign-in')
def create_club(request):
    if request.method == 'POST':
        club_form = ClubForm(request.POST, request.FILES)
        if club_form.is_valid():
            club = club_form.save()
            # Automatically add the creator as a member
            ClubMembership.objects.create(user=request.user, club=club)
            messages.success(request, 'Club created successfully!')
            return redirect('club-list')
    else:
        club_form = ClubForm()
    return render(request, 'create_club.html', {'club_form': club_form})

