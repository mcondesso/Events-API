import time

import requests

from tests.conftest import BASE_URL


def test_health_check():
    # Arrange and act
    response = requests.get(f"{BASE_URL}/health")

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user_creates_user():
    # Arrange: gather data
    username = f"user_{int(time.time() * 1000)}"

    new_user = {
        "username": username,
        "password": "pass1234",
    }

    # Act: create a user with the data
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)

    # Test the response
    assert response.status_code == 201
    assert response.json()["user"]["username"] == new_user["username"]


def test_register_duplicated_user_fails():
    # Arrange: gather data
    username = f"user_{int(time.time() * 1000)}"

    new_user = {
        "username": username,
        "password": "pass1234",
    }

    # Arrange: create a user with the data
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)
    assert response.status_code == 201
    assert response.json()["user"]["username"] == new_user["username"]

    # Act: register duplicated user
    response = requests.post(f"{BASE_URL}/auth/register", json=new_user)

    # Assert
    assert response.status_code == 400


def test_create_public_event_requires_auth_and_succeeds_with_token(auth_token):
    # Arrange
    new_event = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False,
    }

    # Act: Create a new poll
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/events", json=new_event, headers=headers)

    # Test happy path
    assert response.status_code == 201  # Created new resource
    assert response.json()["location"] == new_event["location"]


def test_create_event_requires_auth_token():
    # Arrange
    new_event = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False,
    }

    # Act: Create a new poll
    response_no_token = requests.post(f"{BASE_URL}/events", json=new_event)

    # Test: response is unauthorized
    assert response_no_token.status_code == 401


def test_rsvp_to_public_event_succeeds_without_auth(auth_token):

    # Arrange
    new_event = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False,
    }

    # Arrange: Create a new event with authentication
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/events", json=new_event, headers=headers)
    event_id = response.json()["id"]

    # Act: call RSVP
    rsvp_data = {"attending": True}
    response = requests.post(f"{BASE_URL}/rsvps/event/{event_id}", json=rsvp_data)

    # Test
    assert response.status_code == 201
    assert response.json()["event_id"] == event_id


def test_rsvp_to_non_public_event_fails_without_auth(auth_token):

    # Arrange
    new_event = {
        "title": "Python Meetup",
        "description": "Monthly Python developer meetup",
        "date": "2026-01-15T18:00:00",
        "location": "Tech Hub, Room 101",
        "capacity": 50,
        "is_public": False,
        "requires_admin": False,
    }

    # Arrange: Create a new event with authentication
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BASE_URL}/events", json=new_event, headers=headers)
    event_id = response.json()["id"]

    # Act: call RSVP
    rsvp_data = {"attending": True}
    response = requests.post(f"{BASE_URL}/rsvps/event/{event_id}", json=rsvp_data)

    # Test
    assert response.status_code == 401
    assert response.json().get("error")
