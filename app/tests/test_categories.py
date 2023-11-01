from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.fixture
def create_category(api_client):
    def do_create_category(category):
        return api_client.post("/categories/", category)

    return do_create_category


@pytest.mark.django_db
class TestCreateCategory:
    def test_if_user_is_anonymus_returns_401(self, create_category):
        response = create_category({"title": "a"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
