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

class CampaignJoiningStepOneForm(forms.Form):

    price = forms.IntegerField(
        label="Choisissez un prix",
        min_value=300,
        max_value=1000,
        widget=forms.NumberInput(
            attrs={
                "class": "form-range mx-auto",
                "type": "range",
                "id": "price-slider",
                "oninput": "rangeValue.innerText = this.value"
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        min_price = kwargs.pop("min_price", 300)
        max_price = kwargs.pop("max_price", 1000)
        super(CampaignJoiningStepOneForm, self).__init__(*args, **kwargs)
        self.fields["price"].min_value = min_price
        self.fields["price"].max_value = max_price
        self.fields["price"].widget.attrs.update(
            {
                "min": min_price,
                "max": max_price,
                "value": (max_price - min_price) / 2,
            }
        )

class CampaignJoiningStepTwoForm(forms.Form):
    pass

class CampaignJoiningStepThreeForm(forms.Form):
    pass

class CampaignJoiningStepFourForm(forms.Form):
    pass