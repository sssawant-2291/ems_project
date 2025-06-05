import pytz
from rest_framework import serializers
from django.utils import timezone
from ..models import Event


class EventSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    class Meta:
        model = Event
        fields = ['id', 'name', 'location', 'start_time', 'end_time', 'max_capacity']

    def validate(self, data):
        if Event.objects.filter(
            name=data['name'],
            location=data['location'],
            start_time=data['start_time'],
            end_time=data['end_time']
        ).exists():
            raise serializers.ValidationError("An event with the same name, location, start and end time already exists.")
        return data
    
    def to_representation(self, instance):
        # override output to show converted times
        ret = super().to_representation(instance)
        user_tz = self.context.get('user_timezone', 'UTC')
        tz = pytz.timezone(user_tz)
        ret['start_time'] = timezone.localtime(instance.start_time, tz).isoformat()
        ret['end_time'] = timezone.localtime(instance.end_time, tz).isoformat()
        return ret

