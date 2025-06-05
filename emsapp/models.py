from django.db import models

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'events'
        unique_together = ('name', 'location', 'start_time', 'end_time')


class Guest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'guests'


class GuestEvent(models.Model):
    id = models.AutoField(primary_key=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        db_table = 'events_guests'
        unique_together = ('guest', 'event')

    def __str__(self):
        return f"{self.guest.name} attending {self.event.name}"
