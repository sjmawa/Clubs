from django.contrib import admin
from django.urls import path
from clubs.views import club_list, club_detail, create_club
urlpatterns = [
    path('', club_list, name='club-list'),
    path('<int:club_id>/', club_detail, name='club-detail'),
    path('create/', create_club, name='create-club'),
]
