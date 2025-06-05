from django.urls import path
from .views.event_views import events_handler
from .views.guest_views import register_guest, list_event_attendees

urlpatterns = [
    path('events/', events_handler, name='events_handler'),
    path('events/<int:event_id>/register/', register_guest, name='register-guest'),
    path('events/<int:event_id>/attendees/', list_event_attendees, name='event-attendees'),
]
