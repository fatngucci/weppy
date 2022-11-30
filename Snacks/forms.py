from django import forms
from .models import Snack


class SnackForm(forms.ModelForm):

    class Meta:
        model = Snack
        fields = ['name', 'gewicht', 'beschreibung', 'pictures', 'artikelnummer', 'preis']
        widgets = {
            'hersteller': forms.HiddenInput(),
        }