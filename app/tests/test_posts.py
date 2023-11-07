import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from app.models import Author, Post
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def create_post(api_client):
    def do_create_post(post):
        return api_client.post("/posts/", data=post)

    return do_create_post


@pytest.fixture
def authenticate_user():
    def _authenticate():
        User = get_user_model()
        user = User.objects.create_user(
            username="testuser", password="testShouldBepassword", email="test@email.com"
        )

        # Generate JWT token using Djoser
        response = requests.post(
            "http://127.0.0.1:8000/auth/jwt/create",
            json={"username": "testuser", "password": "testShouldBepassword"},
        )

        if response.status_code == 200:
            token = response.json().get("access")
        else:
            raise ValueError("Failed to generate JWT token")

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        return user

    return _authenticate


@pytest.fixture
def post_data():
    return {
        "title": "Test Post",
        "content": "This is the content of the test post.",
        "category": "Test Category",
    }


@pytest.mark.django_db
class TestCreatePost:
    def test_if_user_is_anonymous_returns_401(self, create_post, post_data):
        response = create_post(post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.skip
    def test_if_user_is_authenticated_can_create_post_returns_201(
        self, authenticate_user, create_post
    ):
        user = authenticate_user()
        author_id = user.author.id
        post_data = {
            "title": "THis is a test from pytest",
            "content": "Busginjsdarhjdiprhsaprhb",
            "category": "1",
            "author": author_id,
        }
        response = create_post(post_data)
        assert response.status_code == status.HTTP_201_CREATED
