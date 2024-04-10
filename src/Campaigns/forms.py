import json
from django import forms

from Campaigns.models import Campaign
from Users.models import CustomUser


# class CollaboratorsField(forms.CharField):
#     def to_python(self, value):
#         if not value:
#             return []
#         try:
#             collaborators = json.loads(value)
#             # Assurez-vous que la valeur est une liste
#             if not isinstance(collaborators, list):
#                 raise forms.ValidationError(
#                     "La valeur doit être une liste de collaborateurs JSON."
#                 )
#             # Vérifiez que chaque collaborateur a les champs "id" et "username"
#             for collaborator in collaborators:
#                 if (
#                     not isinstance(collaborator, dict)
#                     or "id" not in collaborator
#                     or "username" not in collaborator
#                 ):
#                     raise forms.ValidationError(
#                         "Chaque collaborateur doit avoir les champs 'id' et 'username'."
#                     )
#             return collaborators
#         except json.JSONDecodeError:
#             raise forms.ValidationError("La valeur n'est pas un JSON valide.")


class CampaignCreationForm(forms.ModelForm):

    # collaborators = CollaboratorsField(label="Collaborateurs", required=False)

    collaborators = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={}),
        required=False,
        label='Collaborateurs'
    )

    class Meta:
        model = Campaign
        fields = ["name", "start_date", "end_date", "description", "budget", "collaborators"]

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
                attrs={
                    "class": "form-control",
                    "placeholder": "Descriptif de la campagne",
                }
            ),
            "budget": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Rémunération demandée"}
            ),
        }
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["name"].widget.attrs["placeholder"] = "Nom de la campagne"
    #     self.fields["start_date"].widget.attrs["placeholder"] = "Date de début"
    #     self.fields["end_date"].widget.attrs["placeholder"] = "Date de fin"
    #     self.fields["description"].widget.attrs[
    #         "placeholder"
    #     ] = "Description de la campagne"
    #     self.fields["budget"].widget.attrs["placeholder"] = "Budget de la campagne"
        
    # def save(self, commit=True):
    #     campaign = super().save(commit=False)
    #     collaborators_data = self.cleaned_data.get('collaborators', [])
    #     collaborators_ids = [collaborator['id'] for collaborator in collaborators_data]
    #     campaign.collaborators.set(collaborators_ids)
    #     if commit:
    #         campaign.save()
    #     return campaign
