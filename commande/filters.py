import django_filters as df
from django import forms
from client.models import Client
from commande.models import BonLivraisonClinet


class BonLivraisonClinetFilter(df.FilterSet):
    # Filtre par client avec un champ de sélection
    client = df.ModelChoiceFilter(
        field_name='client',
        queryset=Client.objects.all(),
        label='Client',
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-solid form-select-sm',
                "data-control": "select2",
                "data-placeholder": "Sélectionner un client",
                "data-hide-search": "false",
                "size": "1",
                "data-dropdown-auto-width": "true",
            }
        )
    )



    date_livraison = df.DateFilter(
        field_name='date_livraison',
        label='Date de livresion',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        )
    )



    class Meta:
        model = BonLivraisonClinet
        fields = ['client', 'date_livraison']
