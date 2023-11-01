from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register("", views.HomepageViewSet, basename="")
router.register("posts", views.PostViewSet, basename="posts")
router.register("collections", views.CategoryViewSet, basename="collections")
# URLConf
urlpatterns = router.urls
