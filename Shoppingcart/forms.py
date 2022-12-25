from django import forms
from .models import Payment


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