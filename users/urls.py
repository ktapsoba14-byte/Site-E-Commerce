from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('inscription/', views.inscription, name="inscription"),
    path('connexion/', views.connexion, name="connexion"),
    path('Deconnexion/', views.deconnection, name="deconnection"),
    path('client/', views.clients, name="clients"),
    path('client/add/', views.ajout_client, name="ajout_client"),
    path('profil/', views.profil, name="profil"),
    path('contact/', views.contact, name='contact'),
    path('message', views.message, name='message'),
    path('message/<int:pk>/', views.detailmessage, name='detail_message'),
    path('client/modifier/<str:username>', views.modifier_client, name="modifier_client"),
    path('client/supprimer/<str:username>', views.supprimer_client, name="supprimer_client"),
]
