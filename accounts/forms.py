from django import forms
from django.contrib.auth.forms import UserCreationForm

from tree.models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password1', 'email', 'first_name', 'last_name', 'gradation')
