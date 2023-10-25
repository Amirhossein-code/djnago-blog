from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import UserForm, AuthorForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages


# Create your views here.
def homepage(request):
    return HttpResponse("HomePage")


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = AuthorForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ("Your profile was successfully updated!"))
            return redirect("settings:profile")
        else:
            messages.error(request, ("Please correct the error below."))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = AuthorForm(instance=request.user.profile)
    return render(
        request,
        "profiles/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
