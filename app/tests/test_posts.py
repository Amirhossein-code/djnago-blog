import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def create_post(api_client):
    def do_create_post(post):
        return api_client.post("/posts/", post)

    return do_create_post


@pytest.mark.django_db
class TestCreatePost:
    def test_if_user_is_anonymus_returns_401(self , create_post):
        response = create_post({"title": "a"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        