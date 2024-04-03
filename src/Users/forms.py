from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    UserChangeForm,
)

from Users.models import CustomUser, CustomUserProfile

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name in ["password1", "password2"]:
            self.fields[field_name].widget.attrs.update({"class": "form-control"})

    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        label="",
        widget=forms.RadioSelect(
            attrs={"class": "form-check-input form-check-inline", "type": "radio"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = [
            "user_type",
            "username",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Identifiant",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "class": "form-control"}
            ),
            "user_type": forms.CheckboxInput(
                attrs={"class": "form-check-input", "type": "radio"}
            ),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }


class CustomUserUpdateForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email"]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Identifiant",
                    "class": "form-control",
                }
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Email", "class": "form-control"}
            ),
        }


class CustomUserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUserProfile
        fields = [
            "banner",
            "profile_picture",
            "short_description",
            "main_description",
            "instagram_url",
            "x_url",
            "youtube_channel_url",
            "twitch_url",
            "tiktok_url",
            "snapchat_url",
            "contact_mail",
        ]

        widgets = {
            "banner": forms.FileInput(attrs={"class": "form-control", "type": "file"}),
            "profile_picture": forms.FileInput(
                attrs={"class": "form-control", "type": "file"}
            ),
            "short_description": forms.Textarea(
                attrs={"class": "form-control", "rows": "1"}
            ),
            "main_description": forms.Textarea(
                attrs={"class": "form-control", "rows": "3"}
            ),
            "instagram_url": forms.URLInput(
                attrs={
                    "placeholder": "Instagram",
                    "class": "form-control",
                    "type": "url",
                }
            ),
            "x_url": forms.URLInput(
                attrs={
                    "placeholder": "X",
                    "class": "form-control",
                    "type": "url",
                }
            ),
            "youtube_channel_url": forms.URLInput(
                attrs={
                    "placeholder": "Chaîne youtube",
                    "class": "form-control",
                    "type": "url",
                }
            ),
            "twitch_url": forms.URLInput(
                attrs={
                    "placeholder": "Twitch",
                    "class": "form-control",
                    "type": "url",
                }
            ),
            "tiktok_url": forms.URLInput(
                attrs={
                    "placeholder": "Tiktok",
                    "class": "form-control",
                    "type": "url",
                }
            ),
            "snapchat_url": forms.URLInput(
                attrs={
                    "placeholder": "Snapchat",
                    "class": "form-control",
                    "type": "url",
                }
            ),
            "contact_mail": forms.EmailInput(
                attrs={
                    "placeholder": "Email de contact",
                    "class": "form-control",
                    "type": "email",
                }
            ),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Identifiant",
                "class": "form-control",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mot de passe", "class": "form-control"}
        )
    )
