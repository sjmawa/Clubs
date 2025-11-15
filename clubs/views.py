from django.shortcuts import HttpResponse, render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from clubs.models import Club, ClubRole, ClubMembership
from events.models import Event
from clubs.forms import ClubForm, ClubRoleForm
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator

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
    events = Event.objects.filter(club=club).order_by('-date')
    committee = members.filter(role__isnull=False).select_related('user', 'role')

    return render(request, 'club_detail.html', {
        'club': club,
        'members': members,
        'roles': roles,
        'is_member': is_member,
        'events': events,
        'committee': committee
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

def join_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    if request.user.is_authenticated:
        membership, created = ClubMembership.objects.get_or_create(user=request.user, club=club)
        if created:
            messages.success(request, f'You have requested to join {club.name}. Please confirm your membership via the email sent to you.')
        elif not membership.confirmed:
            messages.info(request, f'You have already requested to join {club.name}, please check your email.')
        else:
            messages.info(request, f'You are already a member of {club.name}.')
    else:
        messages.error(request, 'You need to be logged in to join a club.')
    return redirect('club-detail', club_id=club.id)

def confirm_membership(request, membership_id, token):
    membership = get_object_or_404(ClubMembership, id=membership_id, confirmed=False)
    #membership= ClubMembership.objects.get(id=membership_id)
    if membership.confirmed:
        return HttpResponse("Membership already confirmed.")
    if default_token_generator.check_token(membership.user, token):
        membership.confirmed = True
        membership.save()
        return HttpResponse("Membership confirmed!")
    else:
        return HttpResponse("Invalid or expired token.", status=400)
    
@login_required(login_url='sign-in')
def add_role(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    # Optional: restrict to club creator or superuser
    if not request.user.is_superuser and not club.memberships.filter(user=request.user, role__role_name="President").exists():
        messages.error(request, "You are not authorized to add roles.")
        return redirect('club-detail', club_id=club.id)

    if request.method == 'POST':
        form = ClubRoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)
            role.club = club
            role.save()
            messages.success(request, f"Role '{role.role_name}' added successfully!")
            return redirect('club-detail', club_id=club.id)
    else:
        form = ClubRoleForm()

    return render(request, 'add_role.html', {'form': form, 'club': club})
@login_required(login_url='sign-in')
def update_club(request, club_id):
    club = get_object_or_404(Club, id=club_id)

    if not request.user.is_superuser and not club.memberships.filter(user=request.user, role__role_name="President").exists():
        messages.error(request, "You are not authorized to update this club.")
        return redirect('club-detail', club_id=club.id)

    if request.method == 'POST':
        form = ClubForm(request.POST, request.FILES, instance=club)
        if form.is_valid():
            form.save()
            messages.success(request, f"{club.name} updated successfully!")
            return redirect('club-detail', club_id=club.id)
    else:
        form = ClubForm(instance=club)

    return render(request, 'update_club.html', {'club_form': form, 'club': club})
@login_required(login_url='sign-in')
def assign_role(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    members = ClubMembership.objects.filter(club=club, confirmed=True)
    roles = ClubRole.objects.filter(club=club)

    if request.method == 'POST':
        member_id = request.POST.get('member')
        role_id = request.POST.get('role')

        member = get_object_or_404(ClubMembership, id=member_id, club=club)
        role = get_object_or_404(ClubRole, id=role_id, club=club)

        member.role = role
        member.save()
        messages.success(request, f"{member.user.username} has been assigned as {role.role_name}.")
        return redirect('club-detail', club_id=club.id)

    return render(request, 'assign_role.html', {
        'club': club,
        'members': members,
        'roles': roles
    })