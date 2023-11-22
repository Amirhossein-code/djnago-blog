from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from posts.models import Post
from categories.models import Category
from app.models import Author


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=255, required=True)


class SearchPostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
            "tags",
        ]


class SearchCategorySerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "tags",
        ]


class SearchAuthorSerializer(TaggitSerializer, serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Author
        fields = [
            "username",
            "first_name",
            "last_name",
            "bio",
            "profile_image",
            "tags",
        ]
