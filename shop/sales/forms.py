from django import forms
from django.core.exceptions import ValidationError


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


class DeliveryForm(forms.Form):
    new = forms.CharField(
        max_length=4096,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'New shipping address', 'class': 'form-control'}),
    )
    existed = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
    )

    def set_choises(self, customer):
        deliveries = [(0, 'Set new address')]
        deliveries += [(d.id, d.short()) for d in customer.delivery_set.all()]
        self.fields['existed'].choices = deliveries

    def clean_existed(self):
        if self.cleaned_data.get('existed') == '0' and (not self.cleaned_data.get('new')):
            raise ValidationError('Enter new shipping address')
        return self.cleaned_data.get('existed')
