from django.urls import path
from Campaigns.views import *

app_name = "campaigns"

urlpatterns = [
    path(
        "campaigns/create/<int:collaborator_id>/",
        create_campaign,
        name="campaign_creation_with_collab",
    ),
    path(
        "campaigns/create/",
        create_campaign,
        name="campaign_creation",
    ),
    path("campaigns_list/<int:pk>/", get_campaigns_list, name="campaigns_list"),
    path(
        "campaigns_participate_list",
        get_campaigns_participate_list,
        name="campaigns_participate_list",
    ),
    path(
        "campaigns_created_list",
        get_campaigns_created_list,
        name="campaigns_created_list",
    ),
    path("campaign/<int:pk>/", get_campaign_page, name="campaign_page"),
    path(
        "campaigns_requests_list",
        campaign_collaborator_requests,
        name="campaigns_requests_list",
    ),
    path(
        "accept_campaign_collaborator_request/<int:pk>/",
        accept_campaign_collaborator_request,
        name="accept_campaign_collaborator_request",
    ),
    path(
        "refuse_campaign_collaborator_request/<int:pk>/",
        refuse_campaign_collaborator_request,
        name="refuse_campaign_collaborator_request",
    ),
]
