from rest_framework import serializers
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


class AuthorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorReview
        fields = ReviewSerializer.Meta.fields + [
            "author",
        ]
