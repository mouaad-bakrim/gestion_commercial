from django.contrib import admin
from .models import Client, CategoryClient,ClientPrixRel, Fournisseur
from django import forms

# Register the CategoryClient model with default options
@admin.register(CategoryClient)
class CategoryClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class ClientPrixRelInline(admin.TabularInline):
    model = ClientPrixRel
    extra = 1
from django import forms
from .models import Client  # Ensure you import your Client model

class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'  # or specify the fields you want to include

    def clean(self):
        cleaned_data = super().clean()
        affectation_prix_zone = cleaned_data.get('affectation_prix_zone')
        zone = cleaned_data.get('zone')

        # Validate based on the new logic
        if affectation_prix_zone and not zone:
            raise forms.ValidationError("La zone est requise lorsque l'affectation prix zone est activée.")
        elif not affectation_prix_zone and zone:
            raise forms.ValidationError("Si la zone est sélectionnée, l'affectation prix zone doit être activée.")

        return cleaned_data

# Register the Client model with custom options
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm  # Use the custom form for validation
    list_display = ('external_id', 'nom', 'adresse', 'ville', 'formatted_phone', 'actif', 'site', 'category', 'affectation_prix_zone', 'ListePrixVent')
    list_filter = ('actif', 'ville', 'site', 'category')
    search_fields = ('nom', 'external_id', 'phone', 'email', 'cin', 'ice')
    readonly_fields = ('created_at', 'updated_at', 'external_id')
    inlines = [ClientPrixRelInline]

    def formatted_phone(self, obj):
        return obj.formatted_phone

    formatted_phone.short_description = 'Téléphone'


    formatted_phone.short_description = 'Téléphone'
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telephone', 'email', 'site', 'contact_personne')
    list_filter = ('site',)
    search_fields = ('nom', 'telephone', 'email', 'contact_personne')
    ordering = ('-id',)
    fields = ('nom', 'adresse', 'telephone', 'email', 'site', 'contact_personne')
    empty_value_display = '- vide -'

    def has_delete_permission(self, request, obj=None):
        # Optionnel : désactiver la suppression
        return False

admin.site.register(Fournisseur, FournisseurAdmin)

