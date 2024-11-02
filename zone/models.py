from django.db import models
from base.models import Site
from produit.models import Produit





# Model definition for Zone
class Zone(models.Model):
    class Meta:

        verbose_name_plural = "Zones"
        verbose_name = "Zone"
        default_permissions = ['add', 'change', 'view']
        db_table = "zone_zone"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64, unique=True, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    site = models.ForeignKey(Site, on_delete=models.PROTECT, related_name="zones")

    def __str__(self):
        return self.name
