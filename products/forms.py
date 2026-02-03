from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'designation',
            'description',
            'categorie',
            'image',
            "prix_achat",
            "prix_vente",
            "quantite_stock",
            "stock_alerte",
            "en_solde",
            "pourcentage_solde",
        ]