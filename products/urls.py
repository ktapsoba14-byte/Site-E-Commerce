# products/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('propos/', views.propos, name='propos'),
    path('dashbord/', views.dashbord, name='Tableau_de_bord'),
    path('produit/add/', views.ajout_produit, name="ajout_produit"),
    path('produits/', views.produits, name="produits"),
    path('panier/', views.cart, name="panier"),
    path('panier/payements/', views.payement, name='payment'),
    path('panier/delete/', views.delete_cart, name="supression_cart"),
    path('historique-ventes/', views.historique_vente, name='historique_vente'),
    path('tout-historique/', views.tout_historique, name='tout_historique'),
    path('produits/modifier/<str:slug>/', views.modifier_produit, name='modifier_produit'),
    path('produits/supprimer/<str:slug>/', views.supprimer_produit, name='supprimer_produit'),
    path('products/<str:slug>/', views.detail, name="detail"),
    path('facture/<int:order_id>/', views.generer_facture, name='generer_facture'),
    path('produit/<str:slug>/add-to-cart/', views.add_to_cart, name="add-to-cart")
]