from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


from django.utils.functional import lazy


class AbstractBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)


    class Meta:
        abstract = True
        default_permissions = ['add', 'change', 'view', "soft_delete"]

    def soft_delete(self):
        # Get the classes that reference self that are instances of BaseModel and are not soft deleted
        for f in self._meta.get_fields():
            if f.one_to_many or f.one_to_one:
                if issubclass(f.related_model, AbstractBaseModel) and \
                        f.related_model.objects.filter(**{f.field.name: self}, deleted=False).exists():
                    raise ValidationError(
                        "Vous ne pouvez pas supprimer cet élément car il est référencé par au moins un élément de type {0}".format(
                            f.related_model._meta.verbose_name))
        self.deleted = True
        self.save()




class Societe(models.Model):
    FORMES = (
        ('sarl', 'SARL'),
        ('sarlau', 'SARL AU'),
        ('sa', 'SA'),
    )

    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Sociétés"
        default_permissions = ['add', 'change', 'view']
        db_table = "base_company"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name = "Société"
    nom = models.CharField(max_length=30, verbose_name="Raison sociale")
    phone = models.CharField(max_length=16, verbose_name="Téléphone", null=True, blank=True)
    adresse1 = models.CharField(max_length=30, verbose_name="Adresse", null=True, blank=True)
    adresse2 = models.CharField(max_length=30, verbose_name="Suite", null=True, blank=True)
    ville = models.CharField(max_length=15, verbose_name="Ville")
    patente = models.CharField(max_length=15, verbose_name="Patente", null=True, blank=True)
    rc = models.CharField(max_length=15, verbose_name="Registre de commerce", null=True, blank=True)
    cnss = models.CharField(max_length=15, verbose_name="Num CNSS", null=True, blank=True)
    idf = models.CharField(max_length=15, verbose_name="Identifiant fiscal", null=True, blank=True)
    actif = models.BooleanField(default=True, verbose_name="Actif")
    ice = models.CharField(max_length=15, verbose_name="ICE", null=True, blank=True)
    logo = models.ImageField(upload_to='logo', blank=True, null=True, verbose_name="Logo")
    forme = models.CharField(max_length=10, verbose_name="Forme juridique", choices=FORMES, null=True, blank=True)

    def __str__(self):
        if self.forme:
            return "{0} {1}".format(self.nom, self.get_forme_display())
        else:
            return self.nom




class Regions(models.TextChoices):
    MA01 = "MA01", "Tanger-Tétouan-Al Hoceïma"
    MA02 = "MA02", "L'Oriental"
    MA03 = "MA03", "Fès-Meknès"
    MA04 = "MA04", "Rabat-Salé-Kénitra"
    MA05 = "MA05", "Béni Mellal-Khénifra"
    MA06 = "MA06", "Casablanca-Settat"
    MA07 = "MA07", "Marrakech-Safi"
    MA08 = "MA08", "Drâa-Tafilalet"
    MA09 = "MA09", "Souss-Massa"
    MA10 = "MA10", "Guelmim-Oued Noun"
    MA11 = "MA11", "Laâyoune-Sakia El Hamra"
    MA12 = "MA12", "Dakhla-Oued Ed-Dahab"
    ATRE = "ATRE", "Autre / Etranger"


class Site(models.Model):
    class Meta:
        ordering = ["nom"]
        verbose_name_plural = "Sites"
        permissions = (
            ('can_access_hht_parameters', 'Gestion des HHT'),
            ('is_admin_for_hht', 'Mode administrateur pour'),
        )
        default_permissions = ['add', 'change', 'view']
        db_table = "base_site"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verbose_name = "Site"
    nom = models.CharField(max_length=40, verbose_name="Nom")
    phone = models.CharField(max_length=16, verbose_name="Téléphone", null=True, blank=True)
    adresse1 = models.CharField(max_length=30, verbose_name="Adresse", null=True, blank=True)
    adresse2 = models.CharField(max_length=30, verbose_name="Suite", null=True, blank=True)
    ville = models.CharField(max_length=15, verbose_name="Ville", null=True, blank=True)
    patente = models.CharField(max_length=15, verbose_name="Patente", null=True, blank=True)
    ref = models.CharField(max_length=5, verbose_name="Ref")
    actif = models.BooleanField(default=True, null=True, verbose_name="Actif")


    societe_obj = models.ForeignKey(Societe, verbose_name="Société", related_name="sites", on_delete=models.PROTECT,
                                    limit_choices_to={'actif': True})
    region = models.CharField(max_length=6, verbose_name="Région", choices=Regions.choices)



    def __str__(self):
        return self.nom




    def invoice_footer(self, *args, **kwargs):
        first_line = self.societe_obj.nom
        if self.societe_obj.phone:
            first_line += " - Tél: " + self.societe_obj.phone
        elif self.phone:
            first_line += " - Tél: " + self.phone

        if self.societe_obj.ice:
            first_line += " - ICE: " + self.societe_obj.ice
        second_line = ""
        if self.societe_obj.idf:
            second_line += "Identifiant Fiscal: " + self.societe_obj.idf
        if self.patente:
            if second_line != "":
                second_line += " - "
            second_line += "Patente: " + self.societe_obj.patente
        if self.societe_obj.rc:
            if second_line != "":
                second_line += " - "
            second_line += "RC: " + self.societe_obj.rc
        if self.societe_obj.cnss:
            if second_line != "":
                second_line += " - "
            second_line += "CNSS: " + self.societe_obj.cnss

        if second_line == "":
            return ("", first_line)
        return (first_line, second_line)





class Profile(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('superadmin', 'Superadmin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    sites = models.ManyToManyField(Site, blank=True, verbose_name="Sites")


    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def get_user_site(request):
        profile = request.user.profile
        if profile.is_superadmin():
            # Accéder à tous les sites
            sites = Site.objects.all()
        else:
            # Accéder uniquement au site associé au profil
            sites = Site.objects.filter(pk=profile.site.pk)
        return sites


    def is_superadmin(self):
        return self.role == 'superadmin'


