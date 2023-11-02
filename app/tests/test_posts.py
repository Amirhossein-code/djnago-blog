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
    def test_if_user_is_anonymous_returns_401(self, create_post):
        response = create_post({"title": "Test Post", "content": "Lorem ipsum"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_data_is_valid_returns_201(self, authenticate, create_post):
        authenticate()
        response = create_post({"title": "Test Post", "content": "Lorem ipsum"})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_if_user_is_authenticated_can_create_post_returns_201(
        self, authenticate, create_post
    ):
        authenticate()
        response = create_post({"title": "Test Post", "content": "Lorem ipsum"})
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_data_is_invalid_returns_400(self, authenticate, create_post):
        authenticate()
        response = create_post({"title": "", "content": "Lorem ipsum"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None
