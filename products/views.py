# products/views.py
from decimal import Decimal
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from products.forms import ProductForm
from users.models import ContactMessage
from .models import Order, OrderItem, Product, Facture
from django.utils.text import slugify
from .models import Order, OrderItem, Product
from django.contrib.auth import get_user_model
import json
from django.db.models import Count, Sum, F
from decimal import Decimal
from django.db.models.functions import TruncDay




def est_membre_association(user):
    if user and user.is_authenticated:
        if user.est_membre == True or user.is_superuser:
            return True
    return False


#Affichage des produits
def index(request):
    query = request.GET.get('produit')
    categorie_slug = request.GET.get('categorie')
    voir_boutique = request.GET.get('view_as_customer')
    if request.user.is_authenticated and est_membre_association(request.user):
        if not voir_boutique:
            return redirect('Tableau_de_bord')
    products = Product.objects.all()
    if categorie_slug:
        products = products.filter(categorie=categorie_slug)
    categories = Product.CATEGORIE
    return render(request, 'post/index.html', context={"products": products.distinct(), "categories": categories, "query": query})

#detail des produits
def detail(request, slug):
    products = get_object_or_404(Product, slug=slug)
    return render(request, 'post/detail.html', context={'products': products})

#recherche des produits
def produits(request):
    query = request.GET.get('produit')
    if query:
        products_list = Product.objects.filter(designation__icontains=query)
    else:
        products_list = Product.objects.all()
    return render(request, 'post/produits.html', context={'products': products_list,'query': query})

#Ajout des produits
def ajout_produit(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            designation = form.cleaned_data.get('designation')
            slug = slugify(designation)
            if Product.objects.filter(slug=slug).exists():
                messages.error(request, f"Erreur : Le produit '{designation}' existe déjà.")
            else:
                form.save()
                messages.success(request, "Produit ajouté avec succès !")
                return redirect('produits')
    else:
        form = ProductForm()
    return render(request, 'post/ajout_produit.html', {'form': form})

#modifications des produits
def modifier_produit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('produits')
    else:
            form = ProductForm(instance=product)
    return render(request, 'post/ajout_produit.html', {'form': form, 'modifier': True})

#suppressions des produits
def supprimer_produit(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        product.delete()
        return redirect('produits')
    return render(request, 'post/confirmer_suppression.html', {'product': product})

#Ajouter dans le panier
def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        qty_str = request.POST.get('quantite', 1)
        qty = int(qty_str)
    else:
        qty = 1
    order, created = Order.objects.get_or_create(client=user,
                                                est_payee=False)
    order_item, item_created = OrderItem.objects.get_or_create(commande=order,
                                                                produits=product)
    try:
        if not item_created:
            order_item.quantite += qty
        else:
            order_item.quantite = qty
        order_item.save()
        messages.success(request, f"{qty} {product.designation} ajouté(s) au panier.")
    except ValidationError as e:
        messages.error(request, e.messages[0])
    except Exception as e:
        messages.error(request, "Une erreur est survenue lors de l'ajout au panier.")
    order.calculer_et_sauvegarder_total()
    return redirect(reverse('detail', kwargs={"slug": slug}))

#Le panier
def cart(request):
    user = request.user
    order = Order.objects.filter(client=user,
                                 est_payee = False).first()
    return render(request, 'post/panier.html', context={"order": order, 'user':user})

#Suppression du panier
def delete_cart(request):
    user = request.user
    order = Order.objects.filter(client=user,
                                 est_payee=False).first()
    if order:
        order.delete()
    return redirect('index')

#Paiement
def payement(request):
    user = request.user
    order = Order.objects.filter(client=user,
                                 est_payee=False).first()
    if request.method == "POST":
        moyen = request.POST.get('moyen_paiement')
        if moyen == 'CORIS':
            numero_saisi = request.POST.get('numero_coris')
        if moyen == 'ORANGE':
            numero_saisi = request.POST.get('numero_orange')
        elif moyen == 'MOOV':
            numero_saisi = request.POST.get('numero_moov')
        elif moyen == 'CARD':
            numero_saisi = request.POST.get('numero_carte')
        montant_verse_str = request.POST.get('montant_verse', 0)
        montant_verse = Decimal(montant_verse_str) if montant_verse_str else Decimal(0)
        try:
            order.moyen_paiement = moyen
            order.valider_commande()
            facture = order.generer_facture(moyen_paiement=moyen)
            messages.success(request, f"Paiement validé par {moyen} ! Reçu : {facture.numero_recu}")
            return redirect('generer_facture', order_id=order.id)
        except ValidationError as e:
            messages.error(request, f"Erreur : {e.message}")
            return redirect('panier')
    return render(request, 'post/payement.html', {'order': order})

#Facture
def generer_facture(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    facture = getattr(order, 'facture', None)
    if not facture:
        messages.error(request, "Aucune facture trouvée pour cette commande.")
        return redirect('index')
    return render(request, 'post/facture_detail.html', {'order': order,'facture': facture})

#Historique des ventes propre a un client
def historique_vente(request):
    ventes = Order.objects.filter(client=request.user, est_payee=True).order_by('-date_vente')
    return render(request, 'post/historique_ventes.html', {'ventes': ventes})

#Historique de tous les ventes
def tout_historique(request):
    ventes = Order.objects.filter(est_payee=True).order_by('-date_vente')
    return render(request, 'post/tout_historique.html', {'ventes': ventes})

def est_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

#Tableau de board
def dashbord(request):
    User = get_user_model()
    items_payes = OrderItem.objects.filter(commande__est_payee=True)
    chiffre_affaire = Order.objects.filter(est_payee=True).aggregate(total=Sum('montant_total'))['total'] or 0
    total_ventes = Order.objects.filter(est_payee=True).count()
    benefices = items_payes.aggregate(total_benef=Sum(F('quantite') * (F('produits__prix_vente') - F('produits__prix_achat'))))['total_benef'] or 0
    produits_alerte_count = Product.objects.filter(quantite_stock__lte=F('stock_alerte')).count()
    produits_alerte_liste = Product.objects.filter(quantite_stock__lte=F('stock_alerte'))[:5]
    ventes_par_categorie = items_payes.values('produits__categorie').annotate(total_vendus=Sum('quantite')).order_by('-total_vendus')
    label_categorie = [item['produits__categorie'] for item in ventes_par_categorie]
    data_categorie = [int(item['total_vendus']) for item in ventes_par_categorie]
    repartition_payement = Facture.objects.values('moyen_paiement').annotate(nb=Count('id'))
    label_payement = [p['moyen_paiement'] for p in repartition_payement]
    data_payement = [int(p['nb']) for p in repartition_payement]
    stocks_produits = Product.objects.all().order_by('quantite_stock')[:15]
    label_stock = [p.designation for p in stocks_produits]
    data_stock = [p.quantite_stock for p in stocks_produits]
    derniere_factures = Facture.objects.select_related('commande__client').order_by('-date_emission')[:5]
    derniere_client = User.objects.all().order_by('-date_joined')[:3]
    derniers_messages = ContactMessage.objects.all().order_by('-date_envoi')[:3]
    flux_ventes_query = (Order.objects.filter(est_payee=True).annotate(jour=TruncDay('date_vente')).values('jour').annotate(total=Sum('montant_total')).order_by('jour'))
    label_flux = [v['jour'].strftime("%d/%m") for v in flux_ventes_query]
    data_flux = [float(v['total']) for v in flux_ventes_query]
    context = {
        'chiffre_affaire': float(chiffre_affaire),
        'benefices': float(benefices),
        'total_ventes': total_ventes,
        'alerte_count': produits_alerte_count,
        'produits_alerte': produits_alerte_liste,
        'derniere_factures': derniere_factures,
        'derniere_client': derniere_client,
        'derniers_messages': derniers_messages,
        'labels_cat': json.dumps(label_categorie),
        'data_cat': json.dumps(data_categorie),
        'labels_stock': json.dumps(label_stock),
        'data_stock': json.dumps(data_stock),
        'labels_pay': json.dumps(label_payement),
        'data_pay': json.dumps(data_payement),
        'labels_flux': json.dumps(label_flux),
        'data_flux': json.dumps(data_flux),
    }
    return render(request, 'post/dashboard.html', context)

#Apropes
def propos(request):
    return render(request, 'propos.html')

#Contact
def contact(request):
    return render(request, 'contact.html')