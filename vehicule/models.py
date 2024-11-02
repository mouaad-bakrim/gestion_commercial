from django.db import models

from base.models import Site
from produit.models import Produit, ListePrixVent


class Vehicule(models.Model):
    class Meta:
        ordering = ["-_type", "nom"]
        verbose_name_plural = "Véhicules"
        default_permissions = ['add', 'change', 'view']
        db_table = "vehicle_vehicle"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name = "Véhicule"

    CAMION = 'camion'
    MAGASIN = 'magasin'
    TYPES = (
        (CAMION, 'Camion'),
        (MAGASIN, 'Magasin'),
    )

    nom = models.CharField(max_length=30, verbose_name="Nom", unique=True)
    ref = models.CharField(max_length=10, verbose_name="Ref", null=True, blank=True)
    description = models.CharField(max_length=30, verbose_name="Description", null=True, blank=True)
    actif = models.BooleanField(default=True, verbose_name="Actif")
    site = models.ForeignKey(Site, verbose_name="Site", related_name="vehicules", on_delete=models.PROTECT,
                             limit_choices_to={'actif': True})
    _type = models.CharField(max_length=10, verbose_name="Type", choices=TYPES)
    matricule = models.CharField(max_length=20, verbose_name="Matricule", null=True, blank=True)
    ptc = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="PTC (Poids Total en Charge)", help_text="En tonnes")

    # Ensure these fields are defined
    dernier_controle_technique = models.DateField(verbose_name="Dernier contrôle technique", null=True, blank=True)
    prochain_controle_technique = models.DateField(verbose_name="Prochain contrôle technique", null=True, blank=True)

    enable_odometer_checks = models.BooleanField(verbose_name="Activer la relève de l'odomètre?", default=True)
    def __str__(self):
        return f"{self.nom} {self.matricule}"


    @property
    def name_whithout_conducteur(self):
        returned_name = self.nom
        if self.ref:
            returned_name = "[{0}] ".format(self.ref) + returned_name
        return returned_name


class Chauffeur(models.Model):
    class Meta:
        ordering = ['nom']
        verbose_name_plural = "Chauffeurs"
        default_permissions = ['add', 'change', 'view']
        db_table = "chauffeur_chauffeur"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    nom = models.CharField(max_length=50, verbose_name="Nom")
    prenom = models.CharField(max_length=50, verbose_name="Prénom")
    phone = models.CharField(max_length=15, verbose_name="Téléphone", blank=True)
    adresse = models.CharField(max_length=100, verbose_name="Adresse", blank=True)
    site = models.ForeignKey(Site, verbose_name="Site", related_name="chauffeurs", on_delete=models.PROTECT,
                             limit_choices_to={'actif': True})
    actif = models.BooleanField(default=True, verbose_name="Actif")
    vehicule = models.ForeignKey(Vehicule, verbose_name="Véhicule", related_name="chauffeurs",
                                 on_delete=models.PROTECT)
    # Nouveaux attributs ajoutés

    date_embauche = models.DateField(verbose_name="Date d'embauche", null=True, blank=True)
    statut_verification = models.BooleanField(default=False, verbose_name="Statut de vérification")
    date_naissance = models.DateField(verbose_name="Date de naissance", null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    @property
    def full_name(self):
        return f"{self.prenom} {self.nom}"

class Vendeur(models.Model):
    class Meta:
        ordering = ['nom']
        verbose_name_plural = "Vendeurs"
        default_permissions = ['add', 'change', 'view']
        db_table = "vendeur_vendeur"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    external_id = models.CharField(max_length=16, verbose_name="Référence", blank=True)
    nom = models.CharField(max_length=50, verbose_name="Nom")
    prenom = models.CharField(max_length=50, verbose_name="Prénom")
    phone = models.CharField(max_length=15, verbose_name="Téléphone", blank=True)
    adresse = models.CharField(max_length=100, verbose_name="Adresse", blank=True)
    site = models.ForeignKey(Site, verbose_name="Site", related_name="vendeurs", on_delete=models.PROTECT,
                             limit_choices_to={'actif': True})
    actif = models.BooleanField(default=True, verbose_name="Actif")

    vehicule = models.ForeignKey(Vehicule, verbose_name="Véhicule", related_name="Vendeurs",
                                 on_delete=models.PROTECT)

    listPrixVent = models.ForeignKey(ListePrixVent,null=True, blank=True, on_delete=models.PROTECT, verbose_name="Liste de prix")

    date_embauche = models.DateField(verbose_name="Date d'embauche", null=True, blank=True)
    date_naissance = models.DateField(verbose_name="Date de naissance", null=True, blank=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

    def save(self, *args, **kwargs):
        # Générer external_id si ce n'est pas déjà fait
        if not self.external_id:
            # Récupérer le premier caractère du nom
            first_letter = self.nom[0].upper() if self.nom else 'A'

            # Récupérer le code du site (les 3 premières lettres, par exemple)
            site_code = self.site.nom.upper() if self.site else 'XXX'

            # Incrémentation pour l'identifiant
            last_vendeur = Vendeur.objects.filter(external_id__startswith=f"{first_letter}/{site_code}/").order_by(
                'external_id').last()
            next_id = 1 if last_vendeur is None else int(last_vendeur.external_id.split('/')[-1]) + 1

            self.external_id = f"{first_letter}/{site_code}/{next_id:03d}"

            # Vérifier si la longueur est correcte
            if len(self.external_id) > 16:
                raise ValueError("La référence externe dépasse la longueur maximale de 16 caractères.")

        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.prenom} {self.nom}"