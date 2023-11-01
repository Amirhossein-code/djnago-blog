from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("", views.HomepageViewSet, basename="")
router.register("posts", views.PostViewSet, basename="posts")
router.register("categories", views.CategoryViewSet, basename="categories")
router.register("author", views.AuthorViewSet, basename="author")
# URLConf
urlpatterns = router.urls
