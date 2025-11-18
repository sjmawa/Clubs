from django.contrib import admin
from django.urls import path
from events.views import create_event,event_list,event_detail,join_event,leave_event,update_event,delete_event
urlpatterns = [
    path('', event_list, name='event-list'),
    path("create/", create_event, name="create-event"),
    path('<int:event_id>/edit/', update_event, name='update-event'),
    path('<int:event_id>/delete/', delete_event, name='delete-event'),
    path('<int:event_id>/', event_detail, name='event-detail'),
    path('<int:event_id>/join/', join_event, name='join-event'),
    path('<int:event_id>/leave/', leave_event, name='leave-event'),
]
