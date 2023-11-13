from rest_framework import serializers
from .models import AuthorSocialMedia, Post, Category, Author, SocialMediaURL
from taggit.serializers import TagListSerializerField, TaggitSerializer


# Post Serializers
class CreatePostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source="user.author.id", read_only=True)

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


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.id", read_only=True)

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
        ]


class MyPostsSerializer(serializers.ModelSerializer):
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


# Social medi serializers
class SocialMediaURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaURL
        fields = ["url"]


class AuthorSocialMediaSerializer(serializers.ModelSerializer):
    social_media_urls = SocialMediaURLSerializer(many=True)

    class Meta:
        model = AuthorSocialMedia
        fields = ["social_media_urls"]


# sample implementation
# class AuthorSerializer(serializers.ModelSerializer):
#     social_media = AuthorSocialMediaSerializer()

#     class Meta:
#         model = Author
#         fields = ["id", "username", "email", "social_media"]


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


class AuthorSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
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
            "is_liked_by_user",
        ]

    def get_is_liked_by_user(self, obj):
        user = self.context["request"].user
        return obj.is_liked_by_user(user)


class SimpleAuthorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "profile_image",
        ]


class SimpleAuthorWithLikeSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "last_name",
            "bio",
            "profile_image",
            "is_liked_by_user",
        ]

    def get_is_liked_by_user(self, obj):
        user = self.context["request"].user
        return obj.is_liked_by_user(user)
