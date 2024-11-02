from django.contrib import admin
from .models import Vehicule, Vendeur, Chauffeur


class VehiculeAdmin(admin.ModelAdmin):
    list_display = (
        'name_whithout_conducteur', 'ref', 'site', 'actif', '_type', 'matricule', 'ptc',
        'dernier_controle_technique', 'prochain_controle_technique', 'created_at', 'updated_at'
    )
    list_filter = ('site', 'actif', '_type')
    search_fields = ('nom', 'ref', 'description', 'matricule')
    ordering = ['-_type', 'nom']
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

admin.site.register(Vehicule, VehiculeAdmin)



from django.utils.translation import gettext_lazy as _

class VendeurAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('nom', 'prenom', 'phone','adresse')
        }),

        (_('Autre Information'), {
            'fields': ('site', 'actif', 'vehicule', 'listPrixVent'),
            'classes': ('collapse',)
        }),

    )
    list_display = ('full_name', 'phone', 'listPrixVent', 'site', 'actif', 'created_at', 'updated_at')
    list_filter = ('site', 'actif')
    search_fields = ('nom', 'prenom', 'phone')
    ordering = ('nom', 'prenom')
    list_per_page = 20

admin.site.register(Vendeur, VendeurAdmin)




class ChauffeurAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'site', 'actif', 'created_at', 'updated_at')
    list_filter = ('site', 'actif')
    search_fields = ('nom', 'prenom', 'phone')
    ordering = ('nom', 'prenom')
    list_per_page = 20

admin.site.register(Chauffeur, ChauffeurAdmin)