from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from django import forms
from .models import Snack, Comment


class SnackForm(forms.ModelForm):

    class Meta:
        model = Snack
        fields = ('name', 'gewicht', 'beschreibung', 'bilder', 'artikelnummer', 'preis', 'produkt_info')
        widgets = {
            'hersteller': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('gewicht', css_class='form-group col-md-3 mb-0'),
                Column('beschreibung', css_class='form-group col-md-3 mb-0'),
                Column('artikelnummer', css_class='form-group col-md-3 mb-0'),
                Column('preis', css_class='form-group col-md-3 mb-0'),
                Column('bilder', css_class='form-group col-md-3 mb-0'),
                Column('produkt_info', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Add new snack')
        )


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
