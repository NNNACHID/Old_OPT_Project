from django.urls import path
from Campaigns.views import *

app_name = "campaigns"

urlpatterns = [
    path("create/", create_campaign, name="campaign_creation"),
    path("campaigns_list", get_campaigns_list, name="campaigns_list")
]

# htmx_urlpatterns = [
#     path("search_collaborator/", search_collaborator, name="search_collaborator"),
#     path("get_collaborator/", get_collaborator, name="get_collaborator"),
#     path("delete_collaborator/<int:pk>/", delete_collaborator, name="delete_collaborator")
# ]

# urlpatterns += htmx_urlpatterns