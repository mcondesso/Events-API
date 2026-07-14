import time

import pytest
import requests

BASE_URL = "http://localhost:5000/api"


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def auth_token():
    # Arrange: create a unique user
    username = f"user_{int(time.time()*1000)}"

    new_user = {
        "username": username,
        "password": "pass1234",
    }

    # Act: register the user
    requests.post(f"{BASE_URL}/auth/register", json=new_user)

    # Act: login the user
    response = requests.post(f"{BASE_URL}/auth/login", json=new_user)

    # Return the token
    return response.json().get("access_token")
