from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve
from django.utils.html import escape
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required


from Users.models import *
from Users.forms import *


# FROMS METHODS


@require_http_methods(["GET", "POST"])
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.method == "POST":

        form = CustomAuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Données de connexion incorrectes")

    form = CustomAuthenticationForm()
    return render(request, "login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def update_user(request):
    user = request.user
    profile = user.customuserprofile
    if request.method == "POST":

        user_form = CustomUserUpdateForm(request.POST or None, instance=user)
        profile_form = CustomUserProfileForm(
            request.POST or None, request.FILES, instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "User has been updated ! ")
            return redirect("home")
    else:
        user_form = CustomUserUpdateForm(instance=user)
        profile_form = CustomUserProfileForm(instance=profile)
    return render(
        request, "account.html", {"user_form": user_form, "profile_form": profile_form}
    )


def get_profile(request, pk):

    profile = get_object_or_404(CustomUserProfile, user=pk)
    context = {"profile": profile}
    return render(request, "profile.html", context)


def get_users_list(request):
    context = {"users": CustomUser.objects.all()}
    return render(request, "creators_list.html", context)


def get_profile_list_by_type(request):

    url_name = resolve(request.path_info).url_name

    if url_name == "creators":
        context = {
            "profiles": CustomUserProfile.objects.filter(user__user_type="creator")
        }
        return render(request, "creators_list.html", context)
    elif url_name == "advertisers":
        context = {
            "profiles": CustomUserProfile.objects.filter(user__user_type="advertiser")
        }
        return render(request, "advertisers_list.html", context)
    else:
        context = {
            "profiles": CustomUserProfile.objects.filter(user__user_type="association")
        }
        return render(request, "associations_list.html", context)
