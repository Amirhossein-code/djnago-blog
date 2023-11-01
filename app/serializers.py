from rest_framework import serializers
from .models import Post, Collection


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "slug",
            "collection",
            "posted_at",
            "last_updated",
        ]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = [
            "id",
            "name",
        ]
