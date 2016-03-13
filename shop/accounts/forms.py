from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django import forms
import re

# hard phone number template: +xx (xxx) xxxx-xx-xx
PHONE_RG = re.compile(r'^\+\d{,2}\s?\(\d{3}\)\s?\d{3}-?\d{2}-?\d{2}$', re.IGNORECASE)


def phone_validation(value):
    if not PHONE_RG.match(value):
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


class Registration(forms.Form):
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
    password = forms.CharField(
        max_length=64,
        required=True,
        validators=[password_validation.validate_password],
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
    )
    password_confirm = forms.CharField(
        max_length=64,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password confirm', 'class': 'form-control'}),
    )

    def clean_password_confirm(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password_confirm'):
            raise ValidationError('Passwords mismatched')
        return self.cleaned_data.get('password_confirm')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            raise ValidationError('User is already exists')
        return email
