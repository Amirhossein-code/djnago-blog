from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer, CategorySerializer ,AuthorSerializer
from .models import Post, Category , Author


# Create your views here.
class HomepageViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response("Welcome to the homepage")


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer