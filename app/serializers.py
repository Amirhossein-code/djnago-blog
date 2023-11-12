from rest_framework import serializers
from .models import Post, Category, Author


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
    # class Meta:
    #     model = Post
    #     fields = [
    #         "id",
    #         "author",
    #         "title",
    #         "content",
    #         "slug",
    #         "category",
    #         "posted_at",
    #         "last_updated",
    #     ]
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
        read_only_fields = ("author",)

    def to_representation(self, instance):
        # Check if the current user is the owner of the post
        user = self.context["request"].user
        is_owner = user.is_authenticated and user.author == instance.author

        # Exclude the 'author' field if the user is the owner
        if is_owner:
            self.fields.pop("author")

        return super().to_representation(instance)


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
            "id",
            "title",
            "content",
            "category",
        ]


class IntroPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
        ]


# Category serialziers
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "title",
            "slug",
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
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

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
        ]


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
