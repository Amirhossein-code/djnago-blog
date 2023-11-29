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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Manually create hyperlink for the post
        request = self.context.get("request")
        post_url = reverse("posts-detail", args=[str(instance.id)])
        representation["post_url"] = (
            request.build_absolute_uri(post_url) if request else None
        )

        return representation


class SearchCategorySerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "tags",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Manually create hyperlink for the category
        request = self.context.get("request")
        category_url = reverse("categories-detail", args=[str(instance.id)])
        representation["category_url"] = (
            request.build_absolute_uri(category_url) if request else None
        )

        return representation


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Manually create hyperlink for the author
        request = self.context.get("request")
        author_url = reverse("authors-detail", args=[str(instance.id)])
        representation["author_url"] = (
            request.build_absolute_uri(author_url) if request else None
        )

        return representation
