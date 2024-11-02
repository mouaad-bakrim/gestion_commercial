from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Societe, Site, Profile


# Custom Admin for Societe model
@admin.register(Societe)
class SocieteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'forme', 'phone', 'ville', 'actif', 'ice')
    list_filter = ('actif', 'forme', 'ville')
    search_fields = ('nom', 'phone', 'ville', 'ice', 'idf', 'rc')
    readonly_fields = ('created_at', 'updated_at')

    def get_forme(self, obj):
        return obj.get_forme_display()

    get_forme.short_description = 'Forme Juridique'


# Custom Admin for Site model
@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'region', 'phone', 'actif', 'societe_obj')
    list_filter = ('actif', 'ville', 'region')
    search_fields = ('nom', 'phone', 'ville', 'ref')
    readonly_fields = ('created_at', 'updated_at')

    def societe_obj(self, obj):
        return obj.societe_obj.nom

    societe_obj.short_description = 'Société'


# Custom Admin to manage AbstractBaseModel soft delete
class SoftDeleteAdmin(admin.ModelAdmin):
    actions = ['soft_delete_selected']

    def soft_delete_selected(self, request, queryset):
        for obj in queryset:
            try:
                obj.soft_delete()
            except ValidationError as e:
                self.message_user(request, str(e), level='error')
            else:
                self.message_user(request, f"{obj} a été supprimé avec succès.")

    soft_delete_selected.short_description = "Suppression Soft des objets sélectionnés"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'display_sites')
    list_filter = ('role', 'sites')
    search_fields = ('user__username', 'role', 'sites__nom')


    def display_sites(self, obj):
        return ", ".join([site.nom for site in obj.sites.all()])


    display_sites.short_description = "Sites"