from django import forms
from .models import Snack, Comment


class SnackForm(forms.ModelForm):

    class Meta:
        model = Snack
        fields = ('name', 'gewicht', 'beschreibung', 'pictures', 'artikelnummer', 'preis')
        widgets = {
            'hersteller': forms.HiddenInput(),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'sternbewertung': forms.Select(choices=Comment.STERN_BEWERTUNG),
            'poster': forms.HiddenInput(),
            'snack': forms.HiddenInput(),
        }


class SearchForm(forms.ModelForm):

    beschreibung = forms.CharField(required=False)

    class Meta:
        model = Snack
        fields = ['name', 'beschreibung']
