from rest_framework import serializers
from .models import Post, Category
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
    liked_by = serializers.PrimaryKeyRelatedField(read_only=True)

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
            "liked_by",
            "tags",
        ]

    def update(self, instance, validated_data):
        liked_by = validated_data.get("liked_by", None)
        if liked_by and instance.liked_by != liked_by:
            instance.liked_by = liked_by
            instance.save()
        return instance


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
