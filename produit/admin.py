from django.contrib import admin
from .models import ProduitCategorie, Produit, ListePrixAchat, listProduitAchat, ListePrixVent, ListProduitVent
from django.core.exceptions import ValidationError

class ProduitCategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif',)
    search_fields = ('nom',)
    ordering = ('nom',)
    list_per_page = 20



admin.site.register(ProduitCategorie, ProduitCategorieAdmin)

class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'reference', 'prix', 'actif', 'created_at', 'updated_at')
    list_filter = ('actif', 'categorie', 'type_stockage')
    search_fields = ('nom', 'reference')
    ordering = ('categorie', 'nom')
    list_per_page = 20



admin.site.register(Produit, ProduitAdmin)

class listProduitVentInline(admin.TabularInline):
    model = ListProduitVent
    extra = 1

class ListePrixVentAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', 'description')
    search_fields = ('name', 'reference')
    ordering = ('name',)
    inlines = [listProduitVentInline]

# Enregistrement du modèle et de l'administration
admin.site.register(ListePrixVent, ListePrixVentAdmin)


# Inline configuration for listProduitAchat
class listProduitAchatInline(admin.TabularInline):
    model = listProduitAchat  # Correction ici pour utiliser le modèle correct
    extra = 1


# Admin configuration for ListePrixAchat
class ListePrixAchatAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', 'description')
    search_fields = ('name', 'reference')
    ordering = ('name',)
    inlines = [listProduitAchatInline]


# Enregistrement du modèle et de l’administration
admin.site.register(ListePrixAchat, ListePrixAchatAdmin)