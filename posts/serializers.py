from rest_framework import serializers
from .models import Likes, Post, Category
from taggit.serializers import TagListSerializerField, TaggitSerializer


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


class PostLikeSerializer(serializers.Serializer):
    likes = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField()


class PostWithLikeSerializer(serializers.ModelSerializer):
    # Existing serializer fields

    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            user = request.user
            return Likes.objects.filter(user=user, post=obj).exists()
        return False

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "category",
            "is_liked",
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
        serializer = IntroPostSerializer(posts, many=True, read_only=True)
        return serializer.data


class SearchSerializer(serializers.Serializer):
    query = serializers.CharField()
