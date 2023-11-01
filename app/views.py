from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .serializers import PostSerializer
from .models import Post


# Create your views here.
class HomepageViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response("Welcome to the homepage")


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
