from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from posts.models import Post
from categories.models import Category


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
