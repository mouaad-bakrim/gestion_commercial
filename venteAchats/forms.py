from datetime import date
from django import forms
from crispy_forms.helper import FormHelper

from client.models import Client
from produit.models import Produit, ProduitCategorie
from venteAchats.models import Vente, CommandeClient


class CommandeClientForm(forms.ModelForm):
    class Meta:
        model = CommandeClient
        fields = ['article', 'quantite']
        widgets = {
            'prix': forms.NumberInput(attrs={'step': '0.01'}),
            'quantite': forms.NumberInput(attrs={'min': 0}),
        }


class VenteForm(forms.ModelForm):
    articles = forms.ModelMultipleChoiceField(
        queryset=Produit.objects.none(),
        widget=forms.SelectMultiple,
        required=False,
    )

    class Meta:
        model = Vente
        fields = ['client', 'articles']


    def __init__(self, *args, **kwargs):
        user_site = kwargs.pop('user_site', None)
        super(VenteForm, self).__init__(*args, **kwargs)

        # Set today's date as the initial value for date_vente
        if 'date_vente' in self.fields:
            self.fields['date_vente'].initial = date.today()


class VenteCLientListFormHelper(FormHelper):
    model = Vente
    form_tag = False
    form_class = 'd-flex flex-column flex-md-row gap-5'
    field_class = 'flex-row-fluid mae-filter-form'
    help_text_inline = True
    form_show_labels = False