from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import resolve
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


from users.models import *
from users.forms import *


# FROMS METHODS


@require_http_methods(["GET", "POST"])
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Félicitations ! Vous êtes inscris sur la plateforme, connectez-vous pour commencer à trouver de nouvelles collabs !",
            )
            return redirect("home")
        else:
            messages.info(request, "Veuillez remplir le formulaire de manière adéquate.")
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

        service_form = ServiceForm(request.POST or None)

        if user_form.is_valid() and profile_form.is_valid() and service_form.is_valid():
            user_form.save()
            profile_form.save()

            services = []
            prestations = [
                (service_form.cleaned_data["first_prestation"], service_form.cleaned_data["first_prestation_price"]),
                (service_form.cleaned_data["second_prestation"], service_form.cleaned_data["second_prestation_price"]),
                (service_form.cleaned_data["third_prestation"], service_form.cleaned_data["third_prestation_price"]),
            ]

            for name, price in prestations:
                if name and price:
                    services.append({'name': name, 'price': str(price)})  

            profile.services = services
            profile.save()

            messages.success(request, "Profil mis à jour ! ")
            return redirect("home")
    else:
        user_form = CustomUserUpdateForm(instance=user)
        profile_form = CustomUserProfileForm(instance=profile)
        service_form = ServiceForm(
            initial={
                "first_prestation": (
                    profile.services[0]["name"] if profile.services else ""
                ),
                "first_prestation_price": (
                    profile.services[0]["price"] if profile.services else ""
                ),
                "second_prestation": (
                    profile.services[1]["name"] if len(profile.services) > 1 else ""
                ),
                "second_prestation_price": (
                    profile.services[1]["price"] if len(profile.services) > 1 else ""
                ),
                "third_prestation": (
                    profile.services[2]["name"] if len(profile.services) > 2 else ""
                ),
                "third_prestation_price": (
                    profile.services[2]["price"] if len(profile.services) > 2 else ""
                ),
            }
        )
    return render(
        request,
        "account.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "service_form": service_form,
        },
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
        return render(request, "users_list.html", context)
    elif url_name == "advertisers":
        context = {
            "profiles": CustomUserProfile.objects.filter(user__user_type="advertiser")
        }
        return render(request, "users_list.html", context)
    else:
        context = {
            "profiles": CustomUserProfile.objects.filter(user__user_type="association")
        }
        return render(request, "users_list.html", context)
