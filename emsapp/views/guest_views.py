from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from emsapp.models import Event, Guest, GuestEvent
from emsapp.docs.swagger_schemas.guest_views import register_guest_decorator, list_event_attendees_decorator

class AttendeePagination(PageNumberPagination):
    page_size = 10  # default per page
    page_size_query_param = 'page_size'  # allow client to override
    max_page_size = 100

@register_guest_decorator
@api_view(['POST'])
def register_guest(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check for duplicates
    if GuestEvent.objects.filter(event=event, guest__email=request.data.get('email')).exists():
        return Response({"error": "Guest already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

    # Check for capacity
    if GuestEvent.objects.filter(event=event).count() >= event.max_capacity:
        return Response({"error": "Event is fully booked."}, status=status.HTTP_400_BAD_REQUEST)

    guest, _ = Guest.objects.get_or_create(
        email=request.data['email'],
        defaults={'name': request.data['name']}
    )

    # Register the guest for the event
    GuestEvent.objects.create(guest=guest, event=event)

    return Response({
        "message": "Guest registered successfully.",
        "guest": {
            "id": guest.id,
            "name": guest.name,
            "email": guest.email,
        }
    }, status=status.HTTP_201_CREATED)


@list_event_attendees_decorator
@api_view(['GET'])
def list_event_attendees(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    guest_events = GuestEvent.objects.filter(event=event).select_related('guest').order_by('id')

    paginator = AttendeePagination()
    paginated_qs = paginator.paginate_queryset(guest_events, request)

    attendees = [
        {
            "id": ge.guest.id,
            "name": ge.guest.name,
            "email": ge.guest.email
        }
        for ge in paginated_qs
    ]

    return paginator.get_paginated_response(attendees)

