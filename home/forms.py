from django import forms
from django.contrib.auth.models import User

class EmailForm(forms.Form):
    share_to = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )