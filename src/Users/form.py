from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

User = get_user_model()

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2'
        ]