from django import forms


class Profile(forms.Form):
    first_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'First name'}),
    )
    middle_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Middle name'}),
    )
    last_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Last name'}),
    )
    last_name = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Email'}),
    )
    last_name = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Phone number: +xx (xxx) xxxx-xx-xx'}),
    )
