from django import forms
from Snacks.models import Snack, Comment

class SnackEditForm(forms.ModelForm):

    class Meta:
        model = Snack
        fields = ('bilder', 'produkt_info')
        widgets = {
            'snack_id': forms.HiddenInput(),
        }


class CommentEditForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'sternbewertung']
        widgets = {
            'sternbewertung': forms.Select(choices=Comment.STERN_BEWERTUNG),
            'comment_id': forms.HiddenInput()
        }