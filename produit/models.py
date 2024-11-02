from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

class ProduitCategorie(models.Model):
    class Meta:

        verbose_name_plural = "Catégories produits"
        default_permissions = ['add', 'change', 'view']
        verbose_name = "Catégorie produit"
        db_table = "product_category"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nom = models.CharField(max_length = 30, verbose_name = "Nom")
    actif = models.BooleanField(default=True, verbose_name = "Actif")


    def __str__(self):
        return self.nom
    def clean(self):
        if self.pk:
            produits = self.produit_set.filter(actif = True)
            if len(produits)>0 and not self.actif:
                raise ValidationError({'actif': ('Cette catégorie ne peut pas être désactivée. Elle contient au moins un produit')})
        if not self.actif and not self.pk :
            raise ValidationError({'actif': ("L'objet doit être actif lors de sa création.")})

class Produit(models.Model):
    class Meta:
        ordering = ["categorie","nom"]
        verbose_name_plural = "Produits"
        default_permissions = ['add', 'change', 'view']
        db_table = "product_product"
    TYPES = (
        ('stockable', 'Produit stockable'),
        ('consomm', 'Produit consommable'),
        ("service", 'Service'),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    nom = models.CharField(max_length = 32, verbose_name = "Nom")
    nom_court = models.CharField(max_length = 12, verbose_name = "Nom court",null = True, blank = True)
    reference = models.CharField(max_length = 32, verbose_name = "Référence",unique=True)
    prix = models.DecimalField(verbose_name = "Prix public TTC" , default = 0, max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(ProduitCategorie, verbose_name = "Catégorie" , limit_choices_to={'actif': True}, on_delete=models.PROTECT)
    actif = models.BooleanField(default=True, verbose_name = "Actif")
    taux_tva = models.DecimalField(default = 0, verbose_name = "Taux TVA (%)",validators=[MinValueValidator(0),MaxValueValidator(100)] ,
                                                help_text="Entre 0 et 100", max_digits=6, decimal_places=2)
    uom_name = models.CharField(default = "PCE", max_length = 4, verbose_name = "Unité de mesure")
    type_stockage =  models.CharField(max_length = 10, verbose_name = "Type de stockage",choices=TYPES,default = "stockable", db_index=True)

    sub_uom_1_name = models.CharField(default = "UdM2", max_length = 4, verbose_name = "Sous-unité 1 - nom")

    def __str__(self):
        return self.nom
    def clean(self):
        print('cleaning produit')
        if not self.actif and not self.pk :
            raise ValidationError({'actif': ("L'objet doit être actif lors de sa création.")})



class ListProduitVent(models.Model):
    listproduitvent = models.ForeignKey('ListePrixVent', on_delete=models.CASCADE, related_name='list_produit')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='vent_produit')  # Changed related_name
    prix = models.DecimalField(verbose_name="Prix public TTC", default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_list_produit_vent"




class ListePrixVent(models.Model):
    name = models.CharField(max_length=64, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    reference = models.CharField(max_length=5)

    class Meta:
        db_table = "product_list_prix_vent"  # No change here

    def __str__(self):
        return self.name


class ListePrixAchat(models.Model):
    name = models.CharField(max_length=64, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    reference = models.CharField(max_length=5)

    class Meta:
        db_table = "product_list_prix_achat"

    def __str__(self):
        return self.name

class listProduitAchat(models.Model):
    ListePrixAchat = models.ForeignKey('ListePrixAchat', on_delete=models.CASCADE, related_name='list_produit')
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, related_name='achat_produit')  # Changed related_name
    prix = models.DecimalField(verbose_name="Prix public TTC", default=0, max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "product_list_produit_Achat"