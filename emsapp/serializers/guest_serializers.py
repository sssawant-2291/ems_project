from rest_framework import serializers
from ..models import Guest, GuestEvent


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class GuestEventSerializer(serializers.ModelSerializer):
    guest_name = serializers.CharField(source='guest.name', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)

    class Meta:
        model = GuestEvent
        fields = ['id', 'guest', 'guest_name', 'event', 'event_name']
