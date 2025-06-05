import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from emsapp.models import Event, Guest, GuestEvent
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_register_guest():
    client = APIClient()
    event = Event.objects.create(
        name="Webinar",
        location="Online",
        start_time=timezone.now() + timedelta(days=1),
        end_time=timezone.now() + timedelta(days=1, hours=2),
        max_capacity=2
    )

    payload = {
        "name": "John Doe",
        "email": "john@example.com"
    }

    url = reverse('register-guest', args=[event.id])
    response = client.post(url, payload, format="json")
    assert response.status_code == 201
    assert response.data["guest"]["name"] == "John Doe"

@pytest.mark.django_db
def test_prevent_duplicate_guest_registration():
    client = APIClient()
    event = Event.objects.create(
        name="AI Summit",
        location="Delhi",
        start_time=timezone.now() + timedelta(days=2),
        end_time=timezone.now() + timedelta(days=2, hours=2),
        max_capacity=5
    )

    payload = {
        "name": "Alice",
        "email": "alice@example.com"
    }

    url = reverse('register-guest', args=[event.id])
    
    # First registration should succeed
    response1 = client.post(url, payload, format="json")
    assert response1.status_code == 201

    # Second registration with same email for same event should fail
    response2 = client.post(url, payload, format="json")
    assert response2.status_code in [400, 409]
    assert "already registered" in response2.data.get("error", "").lower()


@pytest.mark.django_db
def test_list_event_attendees():
    client = APIClient()
    event = Event.objects.create(
        name="Tech Meetup",
        location="Bangalore",
        start_time=timezone.now() + timedelta(days=1),
        end_time=timezone.now() + timedelta(days=1, hours=2),
        max_capacity=10
    )
    guest = Guest.objects.create(name="Jane", email="jane@example.com")
    GuestEvent.objects.create(event=event, guest=guest)

    url = reverse('event-attendees', args=[event.id])
    response = client.get(url)
    assert response.status_code == 200
    assert any(att["name"] == "Jane" for att in response.data["results"])


@pytest.mark.django_db
def test_attendee_pagination():
    client = APIClient()
    event = Event.objects.create(
        name="Big Event",
        location="Chennai",
        start_time=timezone.now() + timedelta(days=1),
        end_time=timezone.now() + timedelta(days=1, hours=2),
        max_capacity=100
    )
    for i in range(20):
        guest = Guest.objects.create(name=f"Guest {i}", email=f"guest{i}@test.com")
        GuestEvent.objects.create(event=event, guest=guest)

    url = reverse('event-attendees', args=[event.id])
    response = client.get(url, {'page': 1, 'page_size': 10})
    assert response.status_code == 200
    assert "results" in response.data
    assert len(response.data["results"]) == 10
