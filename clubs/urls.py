from django.contrib import admin
from django.urls import path
from clubs.views import club_list, club_detail, create_club,join_club, confirm_membership, add_role
urlpatterns = [
    path('', club_list, name='club-list'),
    path('<int:club_id>/', club_detail, name='club-detail'),
    path('create/', create_club, name='create-club'),
    path('club/<int:club_id>/join/', join_club, name='join-club'),
    path('membership/confirm/<int:membership_id>/<str:token>/',confirm_membership, name='confirm-membership'),
    path('<int:club_id>/add-role/', add_role, name='add-role'),
]
