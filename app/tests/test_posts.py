import pytest
from rest_framework.test import APIClient
from rest_framework import status
from model_bakery import baker
from app.models import Author, Post


@pytest.fixture
def create_post(api_client):
    def do_create_post(post):
        return api_client.post("/posts/", data=post)

    return do_create_post


@pytest.fixture
def post_data():
    post = baker.prepare(Post)
    return {
        "title": post.title,
        "content": post.content,
        "category": post.category,
    }


@pytest.mark.django_db
class TestCreatePost:
    def test_if_user_is_anonymous_returns_401(self, create_post, post_data):
        response = create_post(post_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # def test_if_user_is_authenticated_can_create_post_returns_201(
    #     self, authenticated_user, create_post
    # ):
    #     author = baker.make(Author)

    #     # Get the associated user instance from the Author instance
    #     user = author.user

    #     # Authenticate the user using the authenticated_user fixture
    #     authenticated_user(user)

    #     post_data = {
    #         "title": "Test Post",
    #         "content": "This is a test post",
    #         "category": "tech",
    #     }
    #     response = create_post(post_data)
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert response.data["id"] is not None

    #     assert response.data["title"] == post_data["title"]
    #     assert response.data["content"] == post_data["content"]
    #     assert response.data["category"] == post_data["category"]

    # def test_if_data_is_invalid_returns_400(self, authenticate, create_post):
    #     authenticate()
    #     response = create_post({"title": "", "content": "Lorem ipsum"})
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert response.data["title"] is not None
