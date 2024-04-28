from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Campaigns.models import *
from Campaigns.forms import *

from formtools.wizard.views import SessionWizardView


class CampaignWizardView(SessionWizardView):
    form_list = [
        CampaignCreationStepOneForm,
        CampaignCreationStepTwoForm,
        CampaignCreationStepThreeForm,
    ]
    template_name = "campaign_creation.html"

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        collaborator_id = self.kwargs.get('collaborator_id')
        if collaborator_id and step == '2':
            initial['collaborators'] = [collaborator_id]
        return initial

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        campaign = Campaign(
            name=form_data[0]['name'],
            start_date=form_data[0]['start_date'],
            end_date=form_data[0]['end_date'],
            description=form_data[1]['description'],
            budget=form_data[1]['budget'],
            campaign_creator=self.request.user,
        )
        campaign.save()
        collaborators = form_data[2]["collaborators"]
        for collaborator in collaborators:
            campaign.add_collaborator(collaborator)
        # campaign.collaborators.set(form_data[2]['collaborators'])
        campaign.save()
        messages.success(self.request, "Campagne créer avec succès!")
        return redirect("home")

@login_required(login_url="users:login")
def create_campaign(request, collaborator_id=None):
    wizard_view = CampaignWizardView.as_view()
    return wizard_view(request, collaborator_id=collaborator_id)


@login_required(login_url="users:login")
def get_campaigns_list(request):

    campaigns_with_collaborators = []
    user = request.user

    for campaign in Campaign.objects.all():
        if campaign.campaign_creator == user or user in campaign.collaborators.all():
            campaign_data = {
                "campaign": campaign,
                "collaborators": campaign.collaborators.all(),
            }
            campaigns_with_collaborators.append(campaign_data)

    context = {"campaigns_with_collaborators": campaigns_with_collaborators}
    return render(request, "campaigns_list.html", context)


@login_required(login_url="users:login")
def get_campaigns_participate_list(request):
    campaigns_with_collaborators = []
    user = request.user

    for campaign in Campaign.objects.all():
        if user in campaign.collaborators.all():
            campaign_data = {
                "campaign": campaign,
                "collaborators": campaign.collaborators.all(),
            }
            campaigns_with_collaborators.append(campaign_data)

    context = {"campaigns_with_collaborators": campaigns_with_collaborators}
    return render(request, "campaigns_participate_list.html", context)


@login_required(login_url="users:login")
def get_campaigns_created_list(request):
    campaigns_with_collaborators = []
    user = request.user

    for campaign in Campaign.objects.all():
        if campaign.campaign_creator == user:
            campaign_data = {
                "campaign": campaign,
                "collaborators": campaign.collaborators.all(),
            }
            campaigns_with_collaborators.append(campaign_data)

    context = {"campaigns_with_collaborators": campaigns_with_collaborators}
    return render(request, "campaigns_created_list.html", context)


@login_required(login_url="users:login")
def get_campaign_page(request, pk):

    campaign = get_object_or_404(Campaign, pk=pk)
    context = {"campaign": campaign}
    return render(request, "campaign.html", context)


@login_required(login_url="users:login")
def campaign_collaborator_requests(request):
    requests = CampaignCollaboratorRequest.objects.filter(collaborator=request.user)
    return render(
        request, "campaigns_requests_list.html", {"requests": requests}
    )


@login_required(login_url="users:login")
def accept_campaign_collaborator_request(request_id):
    request_obj = CampaignCollaboratorRequest.objects.get(pk=request_id)
    request_obj.accept()
    return redirect("campaigns:campaigns_list") 


@login_required
def refuse_campaign_collaborator_request(request, pk):
    request_obj = CampaignCollaboratorRequest.objects.get(pk=pk)
    request_obj.decline()
    return redirect("campaigns:campaigns_list")
