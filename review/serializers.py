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
    class Meta:
        model = PostReview
        fields = ReviewSerializer.Meta.fields + [
            "post",
        ]


class AuthorReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorReview
        fields = ReviewSerializer.Meta.fields + [
            "author",
        ]
