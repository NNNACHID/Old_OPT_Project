from django.urls import path
from Users.views import *

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("creators_list/", get_creators_list, name="creators_list"),
    path("advertisers_list/", get_advertisers_list, name="advertisers_list"),
    path("associations_list/", get_associations_list, name="associations_list"),
]
