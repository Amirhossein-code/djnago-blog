from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from posts.models import Post
from categories.models import Category
from app.models import Author
from .validators import validate_query_length
from rest_framework.reverse import reverse


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField(validators=[validate_query_length])


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
