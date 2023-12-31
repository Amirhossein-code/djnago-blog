from django.urls import reverse
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from app.models.category import Category
from app.models.post import Post


# Category serialziers
class CategorySerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "slug",
            "tags",
        ]


class SimplePostSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="category.title")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "category",
            "category_title",
        ]


class CategoryWithPostsSerializer(TaggitSerializer, serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "slug",
            "tags",
            "posts",
        ]

    def get_posts(self, category):
        posts = category.posts.all()
        serializer = SimplePostSerializer(posts, many=True, read_only=True)

        # Manually create hyperlinks for each post
        request = self.context.get("request")

        return [
            {
                "id": post["id"],
                "title": post["title"],
                "category": post["category"],
                "url": request.build_absolute_uri(
                    reverse("posts-detail", args=[str(post["id"])])
                )
                if request
                else None,
            }
            for post in serializer.data
        ]
