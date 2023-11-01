from rest_framework.test import APIClient
from rest_framework import status
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_collection_created_returns_201(self):
        client = APIClient()
        response = client.post("/collections/", {"name": "a"})
        assert response.status_code == status.HTTP_201_CREATED
