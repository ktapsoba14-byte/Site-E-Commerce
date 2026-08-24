# 🛒 UTS'Store - Plateforme E-commerce Django

Bienvenue sur **UTS'Store**, un site web dynamique conçu pour gérer les ventes en ligne d'une association. Cette plateforme e-commerce moderne permet une gestion complète du catalogue de produits, du panier d'achat et des commandes clients.

## ✨ Fonctionnalités

- **📦 Gestion du Catalogue** : Affichage des produits organisés par catégories
- **🛍️ Panier d'Achat** : Ajout, modification et suppression d'articles en temps réel
- **👤 Espace Client** : Inscription, connexion et suivi de l'historique des commandes
- **🔐 Authentification** : Système de gestion des utilisateurs sécurisé
- **⚙️ Interface Admin** : Gestion complète des produits, stocks, prix et commandes via Django Admin
- **💳 Paiement** : Simulation de paiements (Orange Money, Moov Money, etc.)
- **📱 Design Responsif** : Interface adaptée aux appareils mobiles et desktop

## 🛠️ Technologies utilisées

| Composant | Technologie |
|-----------|-------------|
| **Backend** | Django 6.0 (Python) |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Base de données** | SQLite3 |
| **Gestion des images** | Pillow 12.0.0 |
| **ORM** | Django ORM |

## 📋 Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Virtualenv (recommandé)

## 🚀 Installation et Configuration

### 1. Cloner le dépôt

```bash
git clone https://github.com/ktapsoba14-byte/Site-E-Commerce.git
cd Site-E-Commerce
```

### 2. Créer un environnement virtuel

```bash
# Sur Windows
python -m venv .env
.env\Scripts\activate

# Sur macOS/Linux
python3 -m venv .env
source .env/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
DEBUG=True
SECRET_KEY=votre_clé_secrète_django
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Effectuer les migrations de base de données

```bash
python manage.py migrate
```

### 6. Créer un superutilisateur (administrateur)

```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer votre compte administrateur.

### 7. Lancer le serveur de développement

```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : **http://127.0.0.1:8000**

L'interface administrateur : **http://127.0.0.1:8000/admin**

## 📁 Structure du Projet

```
Site-E-Commerce/
├── UTSeSTOR/                 # Application principale Django
│   ├── settings.py          # Configuration Django
│   ├── urls.py              # Routage principal
│   └── wsgi.py              # Configuration WSGI
├── products/                # Application pour la gestion des produits
│   ├── models.py            # Modèles de données
│   ├── views.py             # Vues
│   ├── urls.py              # Routage
│   └── migrations/          # Migrations de base de données
├── users/                   # Application pour la gestion des utilisateurs
│   ├── models.py            # Modèles utilisateur
│   ├── views.py             # Vues d'authentification
│   └── migrations/          # Migrations
├── templates/               # Fichiers HTML
│   ├── base.html            # Template de base
│   ├── products/            # Templates produits
│   └── users/               # Templates utilisateurs
├── static/                  # Fichiers statiques (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── media/                   # Fichiers uploadés (images produits)
├── manage.py                # Fichier de gestion Django
├── db.sqlite3               # Base de données SQLite
├── requirements.txt         # Dépendances Python
└── donnees_backup.json      # Backup des données

```

## 📦 Dépendances Principales

```
Django==6.0              # Framework web
Pillow==12.0.0          # Traitement des images
asgiref==3.11.0         # Support ASGI
sqlparse==0.5.4         # Analyse SQL
```

## 🔧 Commandes Utiles

```bash
# Créer une nouvelle app Django
python manage.py startapp nom_app

# Créer les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic

# Charger les données de backup
python manage.py loaddata donnees_backup.json

# Dumper les données
python manage.py dumpdata > donnees_backup.json

# Shell Django interactif
python manage.py shell

# Lancer les tests
python manage.py test
```

## 📝 Utilisation

### Pour les Administrateurs

1. Accédez à http://127.0.0.1:8000/admin
2. Connectez-vous avec vos identifiants
3. Gérez les produits, catégories, stocks et commandes

### Pour les Clients

1. Visitez la page d'accueil
2. Parcourez les produits par catégorie
3. Ajoutez des articles au panier
4. Complétez vos informations personnelles
5. Simulez le paiement
6. Confirmez votre commande

## 🤝 Contribution

Les contributions sont bienvenues ! Pour contribuer :

1. Créez une branche (`git checkout -b feature/NouvelleFonctionnalité`)
2. Committez vos modifications (`git commit -m 'Ajout de NouvelleFonctionnalité'`)
3. Poussez vers la branche (`git push origin feature/NouvelleFonctionnalité`)
4. Ouvrez une Pull Request

## ⚖️ Licence

Ce projet est fourni tel quel pour usage personnel et éducatif.

## 📧 Contact

Pour toute question ou suggestion, veuillez contacter :
- **Développeur** : ktapsoba14-byte
- **GitHub** : [ktapsoba14-byte](https://github.com/ktapsoba14-byte)

## 🐛 Signaler un Bug

Si vous trouvez un bug, veuillez ouvrir une [issue](https://github.com/ktapsoba14-byte/Site-E-Commerce/issues) avec une description détaillée.

## 📚 Ressources Utiles

- [Documentation Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Pillow Documentation](https://pillow.readthedocs.io/)

---

**Dernière mise à jour** : 24 Août 2026  
**Version** : 1.0.0  
**Statut** : ✅ En développement actif
