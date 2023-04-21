from django import forms
from .models import UserLeaf


class UserLeafForm(forms.ModelForm):
    # status = forms.ChoiceField(choices=UserLeaf.STATUS_CHOICES[:3], label=False)
    class Meta:
        model = UserLeaf
        fields = ['status']
        label_suffix = ''
