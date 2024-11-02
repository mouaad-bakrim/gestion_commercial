from django.db import models
from crum import get_current_user

from base.models import Site
from produit.models import Produit
from produit.models import ListePrixVent



def format_phone(phone_number):
    if not phone_number:
        return ""
    stripped_phone = phone_number.strip().replace(" ","").replace(".","").replace("-","")
    if len(stripped_phone)==10 and stripped_phone.isdigit():
        return "%s%s %s%s %s%s %s%s %s%s" % tuple(stripped_phone)
    elif len(stripped_phone)==13 and stripped_phone.startswith("+212"):
        return "+212 %s %s%s %s%s %s%s %s%s" % tuple(stripped_phone[4:])
    elif len(stripped_phone)==14 and stripped_phone.startswith("00212"):
        return "00 212 %s %s%s %s%s %s%s %s%s" % tuple(stripped_phone[5:])
    else:
        return phone_number.strip()
class CategoryClient(models.Model):

    class Meta:
        verbose_name = "Category Client"
        verbose_name_plural = "Categories Clients"
        db_table = "client_category_client"

    name = models.CharField(max_length=64, verbose_name="Nom")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.name

class Client(models.Model):
    class Meta:
        ordering = ["-updated_at"]
        verbose_name_plural = "Clients"
        permissions = (
            ('can_view_big_picture', 'Can view the big picture'),
            ('view_client_map', 'Can view client maps'),
            ('can_import_client', 'Can import client'),
            ('can_set_client_location', 'Can set client location'),
        )
        default_permissions = ['add', 'change', 'view']
        db_table = "client_client"
        unique_together = ('external_id', 'site')



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nom = models.CharField(max_length=32, verbose_name="Nom")
    adresse = models.CharField(max_length=64, verbose_name="Adresse", blank=True)
    ville = models.CharField(max_length=32, verbose_name="Ville", blank=True)
    phone = models.CharField(max_length=32, verbose_name="Téléphone", blank=True, )
    patente = models.CharField(max_length=16, verbose_name="Patente", blank=True)
    external_id = models.CharField(max_length=16, verbose_name="Référence", blank=True)
    email = models.EmailField(max_length=254, verbose_name="Email", blank=True)  # Champ email ajouté
    cin = models.CharField(max_length=16, verbose_name="CIN", blank=True)
    actif = models.BooleanField(default=True, verbose_name="Actif")
    affectation_prix_zone = models.BooleanField(default=True, verbose_name="Affectation Prix Zone")
    ListePrixVent = models.ForeignKey(ListePrixVent, verbose_name="ListePrixVent", null=True, blank=True, on_delete=models.SET_NULL)
    site = models.ForeignKey(Site, verbose_name="Site", limit_choices_to={'actif': True}, on_delete=models.PROTECT)
    ice = models.CharField(max_length=15, verbose_name="ICE", null=True, blank=True)
    category = models.ForeignKey(CategoryClient, verbose_name="Catégorie", null=True, blank=True,
                                 on_delete=models.SET_NULL)

    def __str__(self):
        return '[%s] %s' % (self.external_id, self.nom)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.pk and user:
            self.created_by_user = user
            self.updated_by_user = user
        elif user:
            self.updated_by_user = user

        if not self.external_id:
            last_client = Client.objects.all().order_by('id').last()
            next_id = 1 if last_client is None else int(last_client.external_id.split('-')[1]) + 1
            self.external_id = f"CL-{next_id:05d}"
        super(Client, self).save(*args, **kwargs)

    @property
    def formatted_phone(self):
        return format_phone(self.phone)



class ClientPrixRel(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='produit_clients')
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='client_produit')
    created_at = models.DateTimeField(auto_now_add=True)
    prix = models.DecimalField(verbose_name="Prix public TTC", default=0, max_digits=10, decimal_places=2)

    class Meta:
        db_table = "client_prix_rel"  # Vérifiez que cela correspond au nom souhaité
        verbose_name = "Relation Client-Prix"
        verbose_name_plural = "Relations Clients-Prix"

    def __str__(self):
        return f"{self.client} - {self.produit} ({self.prix})"


class Fournisseur(models.Model):
    class Meta:
        ordering = ["-id"]
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"
        default_permissions = ['add', 'change', 'view']
        db_table = "user_management_fournisseur"

    nom = models.CharField(max_length=255, unique=True, verbose_name="Nom du fournisseur")
    adresse = models.TextField(verbose_name="Adresse", blank=True, null=True)
    telephone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True, null=True)
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Site")
    contact_personne = models.CharField(max_length=255, verbose_name="Personne de contact", blank=True, null=True)


    def __str__(self):
        return self.nom
