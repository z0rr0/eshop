from django import forms


class OrderForm(forms.Form):
    product = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.HiddenInput(),
    )
    count = forms.IntegerField(
        min_value=1,
        max_value=1000000,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )
