from rest_framework import serializers
from .models import Author
from taggit.serializers import TagListSerializerField, TaggitSerializer
from posts.serializers import SimplePostSerializer
from django.urls import reverse


class AuthorWithPostSerializer(TaggitSerializer, serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    posts = serializers.SerializerMethodField()
    tags = TagListSerializerField()

    class Meta:
        model = Author
        fields = [
            "id",
            "user_id",
            "first_name",
            "last_name",
            "slug",
            "phone",
            "bio",
            "birth_date",
            "profile_image",
            "social_media_url",
            "website_url",
            "tags",
            "posts",
        ]

    def get_posts(self, author):
        posts = author.posts.all()
        serializer = SimplePostSerializer(posts, many=True, read_only=True)

        # Manually create hyperlinks for each post
        request = self.context.get("request")

        return [
            {
                "id": post["id"],
                "title": post["title"],
                "category": post["category"],
                "url": request.build_absolute_uri(
                    reverse("posts-detail", args=[str(post["id"])])
                )
                if request
                else None,
            }
            for post in serializer.data
        ]


class AuthorSerializer(TaggitSerializer, serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    tags = TagListSerializerField()

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
            "social_media_url",
            "website_url",
            "tags",
        ]


class SimpleAuthorSerializer(TaggitSerializer, serializers.ModelSerializer):
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
            "tags",
            "profile_image",
        ]


class SimpleAuthorWithLikeSerializer(serializers.ModelSerializer):
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
            "is_liked_by_user",
        ]
