from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from products.models import Order

class Users(AbstractUser):
    CHOIX_ROLE = (
        ('etudiant', 'Etudiant'),
        ('professeur', 'Professeur'),
        ('personnel', 'Personnel'),
        ('delegue', 'Délégué de promotion')
    )
    role_ecole = models.CharField(max_length=50, choices=CHOIX_ROLE, default='etudiant')
    est_membre = models.BooleanField(default=False)
    est_fidele = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def obtenir_remise_fidelite(self):
        if self.est_fidele:
            return 0.05
        return 0.0

class ContactMessage(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    objet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"Message de {self.nom}  -  {self.objet}"
    class Meta:
        ordering = ['-date_envoi']
