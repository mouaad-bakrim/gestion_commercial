from django.contrib import admin
from .models import Zone



# Admin configuration for Zone
@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'actif', 'site')
    list_filter = ('actif', 'site')
    search_fields = ('name', 'description')


