from django import forms
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    username = forms.CharField(
        label=_("Username"),
        max_length=150,
        required=True,
        widget=forms.TextInput(),
    )
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput(), required=True
    )