from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer
from .models import Post, Category, Author


# Post Serializers
class CreatePostSerializer(TaggitSerializer, serializers.ModelSerializer):
    author_id = serializers.IntegerField(source="user.author.id", read_only=True)
    tags = TagListSerializerField()

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
            "tags",
        ]


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    author = serializers.CharField(source="author.id", read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "slug",
            "category",
            "posted_at",
            "last_updated",
            "tags",
        ]


class MyPostsSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "slug",
            "category",
            "posted_at",
            "last_updated",
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


class IntroPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
        ]


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


class CategoryWithPostsSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "slug",
            "posts",
        ]

    def get_posts(self, category):
        posts = category.posts.all()[:2]
        serializer = IntroPostSerializer(posts, many=True, read_only=True)
        return serializer.data


# Author serialziers
class AuthorWithPostSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    posts = serializers.SerializerMethodField()

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
            "profile_image",
            "posts",
        ]

    def get_posts(self, author):
        posts = author.posts.all()[:2]
        serializer = SimplePostSerializer(posts, many=True, read_only=True)
        return serializer.data


class AuthorSerializer(TaggitSerializer, serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    tags = TagListSerializerField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            "id",
            "user_id",
            "username",
            "first_name",
            "last_name",
            "slug",
            "phone",
            "birth_date",
            "bio",
            "profile_image",
            "tags",
            "is_liked_by_user",
        ]

    def get_is_liked_by_user(self, obj):
        user = self.context["request"].user
        return obj.is_liked_by_user(user)


class SimpleAuthorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    tags = TagListSerializerField()

    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "profile_image",
            "tags",
        ]


class SimpleAuthorWithLikeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    tags = TagListSerializerField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "profile_image",
            "tags",
            "is_liked_by_user",
        ]

    def get_is_liked_by_user(self, obj):
        user = self.context["request"].user
        return obj.is_liked_by_user(user)
