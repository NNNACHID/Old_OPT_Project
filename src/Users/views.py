from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import escape
from django.contrib.auth import get_user_model


from Users.models import *
from Users.forms import *

# def index(request):
#     context = {"users": CustomUser.objects.all()}
#     return render(request, "creator_list.html", context)


def register(request):
    form = CustomUserCreationForm(data=request.POST)
    if request.method == "POST":

        if form.is_valid():
            form.save()
            return redirect("home")

    return render(request, "register.html", {"form": form})

def get_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    profile = get_object_or_404(CustomUserProfile, user=user)
    context = {"profile" : profile, "user" : user}
    return render(request, "profile.html", context)


def set_profile(request, pk):

    form = CustomUserProfileForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("profile", pk=user.pk)


def get_creators_list(request):
    context = {"users": CustomUser.objects.all()}
    return render(request, "creators_list.html", context)


def get_advertisers_list(request):
    context = {"users": CustomUser.objects.all()}
    return render(request, "advertisers_list.html", context)


def get_associations_list(request):
    context = {"users": CustomUser.objects.all()}
    return render(request, "associations_list.html", context)
