from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from emsapp.models import Event
from emsapp.serializers.event_serializers import EventSerializer
from emsapp.docs.swagger_schemas.event_views import get_events_schema, post_events_schema

@get_events_schema
@post_events_schema
@api_view(['GET', 'POST'])
def events_handler(request):
    if request.method == 'GET':
        return list_upcoming_events(request)
    elif request.method == 'POST':
        return create_event(request)

def create_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def list_upcoming_events(request):
    events = Event.objects.filter(start_time__gt=timezone.now())
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)
