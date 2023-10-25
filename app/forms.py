from django import forms
from .models import Author
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = (
            "first_name",
            "last_name",
        )
