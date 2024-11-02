from .models import Client, CategoryClient
import django_filters as df
from django import forms



class ClientListFilter(df.FilterSet):
    # Filtre par nom avec un champ de texte
    nom = df.CharFilter(
        field_name='nom',
        lookup_expr='icontains',
        label='Nom',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nom',
                'class': 'form-control'
            }
        )
    )

    # Filtre par catégorie avec une liste déroulante
    category = df.ModelChoiceFilter(
        queryset=CategoryClient.objects.all(),  # Correct queryset pour les catégories
        label='Catégorie',
        empty_label='--- Catégorie ---',
        widget=forms.Select(
            attrs={
                'class': 'form-select form-select-solid form-select-sm',
                "data-control": "select2",
                "data-placeholder": "Catégorie",
                "data-hide-search": "true",
                "size": "1",
                "data-dropdown-auto-width": "true",
            }
        )
    )

    class Meta:
        model = Client
        fields = ["nom", "category"]
