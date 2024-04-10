from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods
from django.views.generic.list import ListView
from django.contrib import messages

from Campaigns.models import Campaign
from Campaigns.forms import CampaignCreationForm

from Users.models import CustomUser


@login_required(login_url="users:login")
@require_http_methods(["GET", "POST"])
def create_campaign(request):

    if request.method == "POST":
        form = CampaignCreationForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.campaign_creator = request.user
            campaign.save()
            form.save_m2m()  # Pour enregistrer les relations ManyToMany
            messages.success(request, "Campaign has been created!")
            return redirect("home")
    else:
        form = CampaignCreationForm()
    return render(request, "campaign_creation.html", {"form": form})


def get_campaigns_list(request):

    campaigns_with_collaborators = []
    for campaign in Campaign.objects.all():
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    context = {"campaigns_with_collaborators": campaigns_with_collaborators}
    return render(request, "campaigns_list.html", context)


# Dynamic HTMX list for collaborators in the form

# class CollaboratorsList(LoginRequiredMixin, ListView):
#     model = CustomUser
#     template_name = "collaborators_list.html"
#     context_object_name = "collaborators"

#     def get_queryset(self):
#         campaign = self.request.campaign
#         return campaign.collaborators.all()


# def search_collaborator(request):
#     search_text = request.GET.get("search")

#     results = CustomUser.objects.filter(username__icontains=search_text)
#     context = {'results': results}
#     return render(request, 'partials/search_results.html', context)


# def get_collaborator(request):
#     collaborator_username = request.GET.get("username")

#     collaborator = CustomUser.objects.get(username=collaborator_username)
#     # Renvoyer le résultat en tant que JSON
#     return JsonResponse({"id": collaborator.id, "username": collaborator.username})

# def delete_collaborator(request, pk):
#     request.campaign.collaborators.remove(pk)
#     collaborators = request.campaign.collaborators.all()
#     return render(
#         request, "partials/collaborators_list.html", {"collaborators": collaborators}
#     )
