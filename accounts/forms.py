from django import forms
from django.contrib.auth.forms import UserCreationForm

from tree.models import CustomUser


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')