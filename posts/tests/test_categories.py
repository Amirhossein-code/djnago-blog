import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from app.models import Category
from rest_framework.test import APITestCase


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

    def test_if_user_is_authenticated_can_creat_category_returns_201(
        self, authenticate, create_category
    ):
        authenticate()
        response = create_category({"title": "a"})
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_user_is_admin_can_create_category_returns_201(
        self, authenticate, create_category
    ):
        authenticate(is_staff=True)
        response = create_category({"title": "a"})
        assert response.status_code == status.HTTP_201_CREATED

    def test_if_data_is_invalid_returns_400(self, authenticate, create_category):
        authenticate()
        response = create_category({"title": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["title"] is not None
