import json
from django import forms
from django.utils.translation import gettext_lazy as _
from Campaigns.models import Campaign
from Users.models import CustomUser


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
            "budget",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Descriptif de la campagne (facultatif)",
                }
            ),
            "budget": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Proposition d'offre "}
            ),
        }


class CampaignCreationStepThreeForm(forms.ModelForm):
    collaborators = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-select"}
        ),
        required=False,
        label="Collaborateurs",
    )

    class Meta:
        model = Campaign
        fields = ["collaborators"]
