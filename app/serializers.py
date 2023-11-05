from rest_framework import serializers
from .models import Post, Category, Author


class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source="author.id", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author_id",
            "title",
            "content",
            "slug",
            "category",
            "posted_at",
            "last_updated",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "slug",
        ]


class AuthorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Author
        fields = [
            "id",
            "user_id",
            "slug",
            "phone",
            "birth_date",
            "bio",
            "profile_image",
        ]
