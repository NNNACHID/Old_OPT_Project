from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve
from django.utils.html import escape
from django.contrib.auth import get_user_model, login, logout


from Users.models import *
from Users.forms import *

# def index(request):
#     context = {"users": CustomUser.objects.all()}
#     return render(request, "creator_list.html", context)


def register_user(request):
    form = CustomUserCreationForm(data=request.POST)
    if request.method == "POST":

        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        
        username = request.POST["username"]
        password = request.POST["password"]


def logout_user(request):
    logout(request)
    return redirect("home")


def get_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    profile = get_object_or_404(CustomUserProfile, user=user)
    context = {"profile": profile, "user": user}
    return render(request, "profile.html", context)


def set_profile(request, pk):

    form = CustomUserProfileForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("profile", pk=user.pk)


def get_users_list(request):
    context = {"users": CustomUser.objects.all()}
    return render(request, "creators_list.html", context)


def get_users_list_by_type(request):

    url_name = resolve(request.path_info).url_name

    if url_name == "creators":
        context = {"users": CustomUser.objects.filter(user_type="creator")}
        return render(request, "creators_list.html", context)
    elif url_name == "advertisers":
        context = {"users": CustomUser.objects.filter(user_type="advertiser")}
        return render(request, "advertisers_list.html", context)
    else:
        context = {"users": CustomUser.objects.filter(user_type="associations")}
        return render(request, "associations_list.html", context)
