import pytest
from rest_framework.test import APIClient
from emsapp.models import Event
from django.utils import timezone
from datetime import timedelta

@pytest.mark.django_db
def test_create_event():
    client = APIClient()
    payload = {
        "name": "Conference",
        "location": "Mumbai",
        "start_time": "2025-06-10T10:00:00Z",
        "end_time": "2025-06-10T12:00:00Z",
        "max_capacity": 100
    }
    response = client.post("/api/events/", payload, format="json")
    assert response.status_code == 201
    assert response.data["name"] == "Conference"

@pytest.mark.django_db
def test_list_upcoming_events():
    client = APIClient()
    Event.objects.create(
        name="Future Event",
        location="Goa",
        start_time=timezone.now() + timedelta(days=1),
        end_time=timezone.now() + timedelta(days=1, hours=2),
        max_capacity=10
    )
    response = client.get("/api/events/")
    assert response.status_code == 200
    assert len(response.data) > 0

@pytest.mark.django_db
def test_duplicate_event_should_fail():
    client = APIClient()
    payload = {
        "name": "Workshop",
        "location": "Delhi",
        "start_time": "2025-06-15T14:00:00Z",
        "end_time": "2025-06-15T16:00:00Z",
        "max_capacity": 50
    }
    
    # First attempt should succeed
    response1 = client.post("/api/events/", payload, format="json")
    assert response1.status_code == 201

    # Second attempt with same data should fail due to unique constraint
    response2 = client.post("/api/events/", payload, format="json")
    assert response2.status_code == 400 or response2.status_code == 500