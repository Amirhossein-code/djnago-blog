from rest_framework import serializers
from .models import Category
from taggit.serializers import TagListSerializerField, TaggitSerializer
from posts.models import Post


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
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
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
        posts = category.posts.all()[:2]
        serializer = SimplePostSerializer(posts, many=True, read_only=True)
        return serializer.data
