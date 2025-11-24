from django.contrib import admin
from django.urls import path
from core.views import home,search,user_list
urlpatterns = [
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('users/',user_list,name='user-list'),
]
