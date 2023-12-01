from rest_framework_nested import routers
from review.views import AuthorReviewViewSet, PostReviewViewSet
from .views.author_views import AuthorViewSet, HomepageViewSet
from views.post_views import PostViewSet
from views.category_views import CategoryViewSet
from search.views import SearchViewSet

router = routers.DefaultRouter()
router.register("", HomepageViewSet, basename="")
router.register("posts", PostViewSet, basename="posts")
router.register("categories", CategoryViewSet, basename="categories")
router.register("authors", AuthorViewSet, basename="authors")
router.register("search", SearchViewSet, basename="search")

posts_router = routers.NestedDefaultRouter(router, "posts", lookup="post")
posts_router.register("reviews", PostReviewViewSet, basename="post-reviews")

authors_router = routers.NestedDefaultRouter(router, "authors", lookup="author")
authors_router.register("reviews", AuthorReviewViewSet, basename="author-review")

urlpatterns = router.urls + posts_router.urls + authors_router.urls
