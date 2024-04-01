from django.urls import path
from Campaigns.views import *

app_name = "campaigns"

urlpatterns = [
    path("create/", create_campaign, name="campaign_creation"),
]
