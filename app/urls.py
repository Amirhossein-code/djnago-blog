from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("", views.HomepageViewSet, basename="")
router.register("posts", views.PostViewSet, basename="posts")
router.register("categories", views.CategoryViewSet, basename="categories")
router.register("author", views.AuthorViewSet, basename="author")

posts_router = routers.NestedDefaultRouter(router, "posts", lookup="post")
posts_router.register("reviews", views.ReviewViewSet, basename="post-reviews")

# URLConf
urlpatterns = router.urls + posts_router.urls


# For implementing slug endpoints inside Backend
# the Implementation of these endpoints have been transfered to the frontend
# for viewing a specific post based on the post slug       :     /posts/<post-slug>/          Implemented
# for viewwing the specific author based on the author slug :     /authoe/<author-slug>/       Implemented
# for viewing posts of an author                            :     /<author-slug>/<post-slug>/


# from django.urls import path
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register("authors", views.AuthorViewSet, basename="author")
# router.register("posts", views.PostViewSet, basename="post")

# urlpatterns = [
#     # URL pattern for viewing all posts
#     path("posts/", views.PostViewSet.as_view({"get": "list"}), name="all-posts"),
#     # URL pattern for viewing all authors
#     path("authors/", views.AuthorViewSet.as_view({"get": "list"}), name="all-authors"),
#     # URL pattern for viewing a specific post based on the post slug
#     path(
#         "posts/<slug:slug>/",
#         views.PostSlugViewSet.as_view({"get": "retrieve"}),
#         name="post-slug",
#     ),
#     # URL pattern for viewing a specific author based on the author slug
#     path(
#         "authors/<slug:slug>/",
#         views.AuthorSlugViewSet.as_view({"get": "retrieve"}),
#         name="author-slug",
#     ),
# ] + router.urls
