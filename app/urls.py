from rest_framework_nested import routers
from . import views
from review.views import AuthorReviewViewSet, PostReviewViewSet

router = routers.DefaultRouter()
router.register("", views.HomepageViewSet, basename="")
router.register("posts", views.PostViewSet, basename="posts")
router.register("categories", views.CategoryViewSet, basename="categories")
router.register("authors", views.AuthorViewSet, basename="authors")

posts_router = routers.NestedDefaultRouter(router, "posts", lookup="post")
posts_router.register("reviews", PostReviewViewSet, basename="post-reviews")

authors_router = routers.NestedDefaultRouter(router, "authors", lookup="author")
authors_router.register("reviews", AuthorReviewViewSet, basename="author-review")

urlpatterns = router.urls + posts_router.urls + authors_router.urls
