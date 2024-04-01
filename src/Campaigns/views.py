from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib import messages

from Campaigns.forms import CampaignCreationForm


@require_GET
def get_campaign_creation_form(request):
    form = CampaignCreationForm()
    return render(request, "campaign_creation.html", {"form": form})


@require_POST
def submit_campaign_creation_form(request):
    user = request.user
    form = CampaignCreationForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Campaign has been created !")
        return redirect("home")


@login_required(login_url="users:login")
def create_campaign(request):

    http_method = request.method

    match http_method:
        case "GET":
            return get_campaign_creation_form(request)
            
        case "POST":
            return submit_campaign_creation_form(request)


# @require_http_methods(["GET", "POST"])
# @login_required(login_url="login")
# def create(request):
#     user = request.user
#     if request.method == "POST":
#         form = CampaignCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Campaign has been created ! ")
#         return redirect("home")
#     else:
#         form = CampaignCreationForm()
#     return render(request, "campaign_creation.html", {"form": form})
