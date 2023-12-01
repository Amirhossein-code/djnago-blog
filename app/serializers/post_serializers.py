from rest_framework import serializers
from app.models.post import Likes, Post
from app.models.category import Category
from taggit.serializers import TagListSerializerField, TaggitSerializer
from rest_framework.reverse import reverse


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Check if instance.category is not None before creating post_url
        if instance.category:
            # Manually create hyperlink for the post
            request = self.context.get("request")
            post_url = reverse("post-detail", args=[str(instance.id)])
            representation["post_url"] = (
                request.build_absolute_uri(post_url) if request else None
            )
        else:
            # Handle the case where category is None
            representation["post_url"] = None

        return representation


class PostLikeSerializer(serializers.Serializer):
    likes = serializers.IntegerField(read_only=True)
    is_liked = serializers.BooleanField()


class PostWithLikeSerializer(serializers.ModelSerializer):
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
            "id",
            "title",
            "content",
            "category",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Manually create hyperlink for the post
        request = self.context.get("request")
        post_url = reverse("posts-detail", args=[str(instance.id)])
        representation["post_url"] = (
            request.build_absolute_uri(post_url) if request else None
        )

        return representation


class IntroPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
        ]
