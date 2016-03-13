from django.core.exceptions import ValidationError
from django import forms
import re


def phone_validation(value):
    rg = re.compile(r'^\+\d{,2}\s?\(\d{3}\)\s?\d{3}-\d{2}-\d{2}$')
    if not rg.match(value):
        raise ValidationError("incorrect phone number, please use format +xx (xxx) xxxx-xx-xx")


class Profile(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name', 'class': 'form-control'}),
    )
    middle_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Middle name', 'class': 'form-control'}),
    )
    last_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name', 'class': 'form-control'}),
    )
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control'}),
    )
    phone = forms.CharField(
        validators=[phone_validation],
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '+xx (xxx) xxxx-xx-xx', 'class': 'form-control'}),
    )
