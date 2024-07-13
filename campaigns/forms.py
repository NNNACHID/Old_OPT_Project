import json
from django import forms
from django.utils.translation import gettext_lazy as _
from campaigns.models import Campaign
from users.models import CustomUser


class CampaignCreationStepOneForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = ["name", "start_date", "end_date"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": _("Nom de la campagne")}
            ),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "placeholder": _("Début de la campagne")}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "placeholder": _("Fin de la campagne")}
            ),
        }

        labels = {
            "name": _("Nom"),
            "start_date": _("Début"),
            "end_date": _("Fin"),
        }

class CampaignCreationStepTwoForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = [
            "description",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descriptif de la campagne (facultatif)",
                }
            )
        }


class CampaignCreationStepThreeForm(forms.ModelForm):

    class Meta:
        model = Campaign
        fields = []

    min_price = forms.IntegerField(
        label="Minimum price",
        widget=forms.HiddenInput(
            attrs={
                "type": "hidden",
                "id": "id_price_min",
                "value": "200"
            }
        ),
    )
    max_price = forms.IntegerField(
        label="Maximum price",
        widget=forms.HiddenInput(
            attrs={
                "type": "hidden",
                "id": "id_price_max",
                "value": "800"
            }
        ),
    )
    # min_price = forms.IntegerField(label="Minimum Price", widget=forms.HiddenInput())
    # max_price = forms.IntegerField(label="Maximum Price", widget=forms.HiddenInput())

class CampaignJoinForm(forms.Form):

    price = forms.IntegerField(
        label="Choisissez un prix",
        min_value=300,
        max_value=1000,
        widget=forms.NumberInput(
            attrs={
                "class": "form-range mx-auto",
                "type": "range",
                "min": "300",
                "max": "1000",
                "value": "300",
                "id": "price-slider",
                "oninput": "rangeValue.innerText = this.value"
            }
        ),
    )
