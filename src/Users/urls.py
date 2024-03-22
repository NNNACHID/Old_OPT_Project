from django.urls import path
from Users.views import *

app_name = "users"

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("creators_list/", get_users_list_by_type, name="creators"),
    path("advertisers/", get_users_list_by_type, name="advertisers"),
    path("associations/", get_users_list_by_type, name="associations"),
    path("profile/<int:user_id>/", get_profile, name="profile"),
]
