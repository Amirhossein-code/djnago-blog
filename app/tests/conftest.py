import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))

    return do_authenticate


@pytest.fixture
def authenticated_user(api_client):
    def _authenticate(user):
        api_client.force_authenticate(user=user)
        return user

    return _authenticate
