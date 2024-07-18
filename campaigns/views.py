from django.http import JsonResponse
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from campaigns.models import *
from campaigns.forms import *

from formtools.wizard.views import SessionWizardView

CREATION_FORMS = [
    CampaignCreationStepOneForm,
    CampaignCreationStepTwoForm,
    CampaignCreationStepThreeForm
]

JOINING_FORMS = [
    CampaignJoiningStepOneForm,
    CampaignJoiningStepTwoForm
]


class CampaignCreationWizardView(SessionWizardView):
    form_list = CREATION_FORMS
    template_name = "campaign_creation.html"

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        campaign = Campaign(
            name=form_data[0]["name"],
            start_date=form_data[0]["start_date"],
            end_date=form_data[0]["end_date"],
            description=form_data[1]["description"], 
            # min_price=form_data[2]["min_price"],
            # max_price=form_data[2]["max_price"],
            campaign_creator=self.request.user,
        )
        
        campaign.save()
        messages.success(self.request, "Campagne créée avec succès!")
        return redirect("home")

class CampaignJoiningWizardView(SessionWizardView):
    form_list = JOINING_FORMS
    template_name = "join_campaign.html"

    def done(self, form_list, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        collaboration_request = CampaignCollaboratorRequest(
            message=form_data[0]["message"],
            campaign=self.kwargs.get('campaign'),
            collaborator=self.request.user
        )
        
        collaboration_request.save()
        messages.success(self.request, "Demande de participation envoyer !")
        return redirect("home")


@login_required(login_url="users:login")
def create_campaign(request, collaborator_id=None):
    wizard_view = CampaignCreationWizardView.as_view()
    return wizard_view(request, collaborator_id=collaborator_id)

@login_required
def join_campaign(request, campaign_pk, campaign_user_pk):

    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    campaign_page_user = get_object_or_404(CustomUser, pk=campaign_user_pk)
    wizard_view = CampaignJoiningWizardView.as_view()
    return wizard_view(request, campaign=campaign)

@login_required(login_url="users:login")
def get_campaigns_list(request, pk):

    user = get_object_or_404(CustomUser, pk=pk)
    campaigns_with_collaborators = []

    campaigns_created = Campaign.objects.filter(campaign_creator=user)
    for campaign in campaigns_created:
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    collaborations = Campaign.objects.filter(collaborators=user)
    for campaign in collaborations:
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    context = {
        "campaigns_with_collaborators": campaigns_with_collaborators,
        "campaign_page_user": user,
    }
    return render(request, "campaigns_list.html", context)


@login_required(login_url="users:login")
def get_campaigns_participate_list(request, pk):
    campaigns_with_collaborators = []
    user = get_object_or_404(CustomUser, pk=pk)

    collaborations = Campaign.objects.filter(collaborators=user)
    for campaign in collaborations:
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    context = {
        "campaigns_with_collaborators": campaigns_with_collaborators,
        "campaign_page_user": user,
    }
    return render(request, "campaigns_participate_list.html", context)


@login_required(login_url="users:login")
def get_campaigns_created_list(request, pk):

    user = get_object_or_404(CustomUser, pk=pk)
    campaigns_with_collaborators = []

    campaigns_created = Campaign.objects.filter(campaign_creator=user)
    for campaign in campaigns_created:
        campaign_data = {
            "campaign": campaign,
            "collaborators": campaign.collaborators.all(),
        }
        campaigns_with_collaborators.append(campaign_data)

    context = {
        "campaigns_with_collaborators": campaigns_with_collaborators,
        "campaign_page_user": user,
    }
    return render(request, "campaigns_created_list.html", context)


@login_required(login_url="users:login")
def get_campaign_page(request, campaign_pk, campaign_user_pk):

    campaign = get_object_or_404(Campaign, pk=campaign_pk)
    user = get_object_or_404(CustomUser, pk=campaign_user_pk)

    collaborators = campaign.collaborators.all()

    context = {
        "campaign": campaign,
        "collaborators": collaborators,
        "campaign_page_user": user,
    }
    return render(request, "campaign.html", context)


@login_required(login_url="users:login")
def campaign_collaborator_requests(request):
    user = request.user
    user_campaigns = Campaign.objects.filter(campaign_creator=user)
    requests = []
    collaboration_requests = CampaignCollaboratorRequest.objects.all()
    for campaign in user_campaigns:
        for collaboration_request in collaboration_requests:
            if collaboration_request.campaign == campaign:
                requests.append(collaboration_request)

    context = {
        "requests": requests,
        "campaign_page_user": user,
    }
    return render(request, "campaigns_requests_list.html", context)


# @login_required(login_url="users:login")
# def accept_campaign_collaborator_request(request, request_id):
#     request_obj = CampaignCollaboratorRequest.objects.get(pk=request_id)
#     stripe.api_key = settings.STRIPE_SECRET_KEY
#     campaign = get_object_or_404(Campaign, id=request_obj.campaign_id)
#     campaign_budget = int(campaign.budget)
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=["card"],
#         line_items=[
#             {
#                 "price_data": {
#                     "currency": "eur",
#                     "unit_amount": campaign_budget,
#                     "product_data": {"name": campaign.name},
#                 },
#                 "quantity": 1,
#             },
#         ],
#         mode="payment",
#         success_url=request.build_absolute_uri(
#             reverse("campaigns:campaigns_list", kwargs={"pk": request.user.pk})
#         ),
#         cancel_url=request.build_absolute_uri(
#             reverse("campaigns:campaigns_requests_list")
#         )
#     )
#     messages.info(request, "Paiement éffectué !")
#     # request_obj.accept()
#     return redirect(checkout_session.url)


@login_required(login_url="users:login")
def accept_campaign_collaborator_request(request, request_id):
    request_obj = CampaignCollaboratorRequest.objects.get(pk=request_id)
    campaign = get_object_or_404(Campaign, id=request_obj.campaign_id)
    messages.info(request, "Paiement éffectué !")
    request_obj.accept()
    return redirect("home")


@login_required
def refuse_campaign_collaborator_request(request_id):
    request_obj = CampaignCollaboratorRequest.objects.get(pk=request_id)
    request_obj.decline()
    return redirect("campaigns:campaigns_list")
