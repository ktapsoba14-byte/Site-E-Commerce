from decimal import Decimal
import uuid
from django.db import models, transaction
from django.forms import ValidationError
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone


class Product(models.Model):
    CATEGORIE = [
        ('TSHIRT','tshirt'),
        ('BASQUET', 'basquet'),
        ('ORDINATEUR', 'ordinateur'),
        ('AUTRE', 'autre'),
    ]
    designation = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=100)
    categorie = models.CharField(max_length=10, choices=CATEGORIE, default='TSHIRT', verbose_name="Categorie des produits")
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name="Description détaillée")
    image = models.ImageField(upload_to="products_images", blank=True, null=True, verbose_name="Images du produits")
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Prix d'achat")
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True, verbose_name="Prix de vente")
    quantite_stock = models.IntegerField(default=0, verbose_name="Quantité en stock")
    stock_alerte = models.IntegerField(default=10, verbose_name="Seuil en alerte")
    en_solde = models.BooleanField(default=False, verbose_name="Produit en solde")
    pourcentage_solde = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, verbose_name="Pourcentage de réduction")

    def __str__(self):
        return self.designation
    def prix_vente_actuel(self):
        if self.en_solde and self.pourcentage_solde > 0:
            reduction = self.prix_vente * (self.pourcentage_solde / 100)
            return self.prix_vente - reduction
        return self.prix_vente
    def alerte(self):
        return self.quantite_stock <= self.stock_alerte
    def save(self, *args, **kwargs):
        if not self.slug and self.designation:
            self.slug = slugify(self.designation)
        super(Product, self).save(*args, **kwargs)

class Order(models.Model):
    MOYENS_PAIEMENT = [
        ('CORIS', 'Coris Money'),
        ('ORANGE', 'Orange Money'),
        ('MOOV', 'Moov Money'),
        ('CARD', 'Carte Bancaire'),
    ]
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Nom du client")
    date_vente = models.DateTimeField(auto_now_add=True, verbose_name="Date de vente")
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Prix de vente total")
    reduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Réduction pour fidélité")
    moyen_paiement = models.CharField(max_length=10, choices=MOYENS_PAIEMENT, default='ORANGE', verbose_name="Numéro de téléphone/Carte")
    montant_verse = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Montant reçu")
    montant_rendu = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Monnaie rendue")
    est_payee = models.BooleanField(default=False, verbose_name="Statut du paiement")

    def __str__(self):
        return f"commande {self.id} - {self.client.username} ({self.date_vente.strftime('%d/%m/%Y')})"

    def valider_commande(self):
        with transaction.atomic():
            for item in self.items.all():
                if item.produits.quantite_stock < item.quantite:
                    raise ValidationError(f"Plus assez de {item.produits.designation}")
                item.produits.quantite_stock -= item.quantite
                item.produits.save()
            self.est_payee = True
            self.save()

    def generer_facture(self, moyen_paiement):
        if self.est_payee:
            facture, created = Facture.objects.get_or_create(
                commande=self,
                defaults={
                    'moyen_paiement': moyen_paiement,
                    'numero_recu': f"FAC-{self.id}-{self.date_vente.strftime('%y%m%d')}"
                }
            )
            return facture
        return None

    def calculer_et_sauvegarder_total(self):
        total_brut = sum(item.get_total_ligne() for item in self.items.all())
        remise_volume = Decimal('0.00')
        if total_brut > 20000:
            remise_volume = total_brut * Decimal('0.05')
        remise_fidelite_pourcent = Decimal(str(self.client.obtenir_remise_fidelite()))
        remise_fidelite_valeur = total_brut * remise_fidelite_pourcent
        self.reduction = remise_volume + remise_fidelite_valeur
        self.montant_total = total_brut - self.reduction
        self.save()

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

class OrderItem(models.Model):
    commande = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    produits = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def get_total_ligne(self):
        return self.quantite * self.produits.prix_vente_actuel()
    def save(self, *args, **kwargs):
        if self.produits.quantite_stock < self.quantite:
            raise ValidationError(f"Stock insuffisant ({self.produits.quantite_stock} dispos)")
        super().save(*args, **kwargs)

class Facture(models.Model):
    MOYENS_PAIEMENT = [
        ('CORIS', 'Coris Money'),
        ('ORANGE', 'Orange Money'),
        ('MOOV', 'Moov Money'),
        ('CARD', 'Carte Bancaire'),
    ]
    commande = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="facture")
    numero_recu = models.CharField(max_length=20, unique=True, editable=False)
    moyen_paiement = models.CharField(max_length=10, choices=MOYENS_PAIEMENT, default='CASH')
    date_emission = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.numero_recu:
            date_str = timezone.now().strftime('%Y%m%d')
            unique_id = uuid.uuid4().hex[:4].upper()
            self.numero_recu = f"REC-{date_str}-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Facture {self.numero_recu} (Commande {self.commande.id})"