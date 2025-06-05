import pytest
from emsapp.models import Event, Guest, GuestEvent
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_event_str():
    event = Event(name="Demo", location="Pune", start_time=timezone.now(), end_time=timezone.now() + timedelta(hours=2), max_capacity=100)
    assert str(event) == "Demo"

@pytest.mark.django_db
def test_guest_creation():
    guest = Guest.objects.create(name="Nipun", email="Nipun@email.com")
    assert guest.name == "Nipun"

@pytest.mark.django_db
def test_guest_event_link():
    event = Event.objects.create(name="Test", location="Delhi", start_time=timezone.now(), end_time=timezone.now() + timedelta(hours=1), max_capacity=10)
    guest = Guest.objects.create(name="Pratik", email="Pratik@email.com")
    ge = GuestEvent.objects.create(event=event, guest=guest)
    assert ge.event.name == "Test"
    assert ge.guest.email == "Pratik@email.com"
