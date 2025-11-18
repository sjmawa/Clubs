from django.contrib import admin
from django.urls import path
from core.views import home,search
urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
]
