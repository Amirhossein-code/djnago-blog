from rest_framework import serializers
from app.models.author import Author
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
    # user id of the person who posted the review
    user = serializers.ReadOnlyField(source="user.username")
    # author id of the person who posted the review
    author_id_posting_review = serializers.ReadOnlyField(source="user.author.id")
    # author that is being reviewed
    author_id_being_reviewed = serializers.SerializerMethodField()
    # author dose the same thing as above line but the naming is misleading

    class Meta:
        model = AuthorReview
        fields = ReviewSerializer.Meta.fields + [
            "author",
            "author_id_being_reviewed",
            "author_id_posting_review",
        ]

    def get_author_id_being_reviewed(self, obj):
        return self.context.get("author_id")
