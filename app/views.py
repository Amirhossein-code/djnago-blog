from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response


# Create your views here.
class HomepageViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response("Welcome to the homepage")
