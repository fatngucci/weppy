from django import forms
from Snacks.models import Snack

class SnackEditForm(forms.ModelForm):

    class Meta:
        model = Snack
        fields = ('bilder', 'produkt_info')
        widgets = {
            'snack_id': forms.HiddenInput(),
        }