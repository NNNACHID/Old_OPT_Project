from django import forms

from Campaigns.models import Campaign


class CampaignCreationForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ["name", "start_date", "end_date", "description", "budget"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nom de la campagne"}
            ),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "placeholder": "Début de la campagne"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "placeholder": "Fin de la campagne"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Descriptif de la campagne"}
            ),
            "budget": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Rémunération demandée"}
            ),
        }
