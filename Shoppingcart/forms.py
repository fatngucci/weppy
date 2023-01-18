from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Div, Submit
from django import forms

from .models import Payment, ShoppingCartItem


class PaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['betrag'].widget.attrs['readonly'] = True

    class Meta:
        model = Payment
        fields = ['kreditkartenr', 'ablaufsdatum', 'betrag']
        widgets = {
            'benutzer': forms.HiddenInput(),
        }


class AddForm(forms.ModelForm):
    class Meta:
        model = ShoppingCartItem
        fields = ['menge']
        widgets = {
            'produkt_id': forms.HiddenInput()
        }
