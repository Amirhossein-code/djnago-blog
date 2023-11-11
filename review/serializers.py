from rest_framework import serializers

from app.models import Author
from .models import PostReview, AuthorReview, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "rating",
            "comment",
            "created_at",
        ]


class PostReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = PostReview
        fields = ReviewSerializer.Meta.fields + []

    def create(self, validated_data):
        post_id = self.context.get("post_id")
        user = self.context.get("user")

        validated_data["post_id"] = post_id
        validated_data["user"] = user

        return super().create(validated_data)


class RetrievePostReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    author_id = serializers.ReadOnlyField(source="user.author.id")

    class Meta:
        model = PostReview
        fields = ReviewSerializer.Meta.fields + ["post", "author_id"]


class AuthorReviewSerializer(serializers.ModelSerializer):
    # This end point is bugged a single reviwe of an author is visble at other end points
    # fix later
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = AuthorReview
        fields = ReviewSerializer.Meta.fields + []

    def create(self, validated_data):
        author_id = self.context.get("author_id")
        user = self.context.get("user")

        author = Author.objects.get(id=author_id)

        validated_data["author"] = author
        validated_data["user"] = user

        return super().create(validated_data)


class RetrieveAuthorReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    # author_id = serializers.ReadOnlyField(source="user.author.id")
    author_id = serializers.ReadOnlyField(source="author.id")
    author = serializers.StringRelatedField()

    class Meta:
        model = AuthorReview
        fields = ReviewSerializer.Meta.fields + ["author", "author_id"]
