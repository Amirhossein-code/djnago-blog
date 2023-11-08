from rest_framework import serializers
from .models import AuthorProfileImage, Post, Category, Author


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


class SimplePostSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="author.first_name")
    last_name = serializers.CharField(source="author.last_name")

    class Meta:
        model = Post
        fields = [
            "id",
            "first_name",
            "last_name",
            "title",
            "content",
            "category",
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
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    # profile_image = serializers.ImageField(source='author.profile_')
    class Meta:
        model = Author
        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "slug",
            "phone",
            "birth_date",
            "bio",
            # "profile_image",
        ]


class AuthorProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorProfileImage
        fields = [
            "id",
            "author",
            "image",
        ]
