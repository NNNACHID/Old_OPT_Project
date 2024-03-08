from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from Users.models import CustomUser

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "user_type",
        )
