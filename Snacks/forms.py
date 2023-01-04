from django import forms
from .models import Snack, Comment


class SnackForm(forms.ModelForm):

    class Meta:
        model = Snack
        fields = ('name', 'gewicht', 'beschreibung', 'bilder', 'artikelnummer', 'preis', 'produkt_info')
        widgets = {
            'hersteller': forms.HiddenInput(),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'sternbewertung']
        widgets = {
            'sternbewertung': forms.Select(choices=Comment.STERN_BEWERTUNG),
            'poster': forms.HiddenInput(),
            'snack': forms.HiddenInput(),
        }

class CommentEditForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'sternbewertung']
        widgets = {
            'sternbewertung': forms.Select(choices=Comment.STERN_BEWERTUNG),
            'comment_id': forms.HiddenInput()
        }


class SearchForm(forms.ModelForm):

    beschreibung = forms.CharField(required=False)
    produkt_bewertung = forms.DecimalField(required=False)

    class Meta:
        model = Snack
        fields = ['name', 'beschreibung', 'produkt_bewertung']
