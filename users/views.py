from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render, get_object_or_404
from users.forms import UserForm
from users.models import ContactMessage, Users
from django.contrib.messages import get_messages
#Client
#Affichages des clients
def clients(request):
    query = request.GET.get('client', '')
    if query:
        client_list = Users.objects.filter(username__icontains=query)
    else:
        client_list = Users.objects.all()
    return render(request, 'comptes/clients.html', context={'clients': client_list,'query': query})
#  Inscription pour un nouveau clien
def inscription(request):
    if request.method == 'POST':
        nom_utilisateur = request.POST.get('username')
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('password')
        nom = request.POST.get('first_name')
        prenom = request.POST.get('last_name')
        role = request.POST.get('role_ecole')
        user = Users.objects.create_user(username=nom_utilisateur,
                                        email=email,
                                        password=mot_de_passe,
                                        first_name = nom,
                                        last_name=prenom,
                                        role_ecole = role)
        login(request, user)
        return redirect('connexion')
    return render(request, 'comptes/signup.html')
#Connection
def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            storage = get_messages(request)
            for message in storage:
                pass
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'comptes/login.html')
#Deconnections
def deconnection(request):
    storage = get_messages(request)
    for _ in storage:
        pass
    logout(request)
    return redirect('index')
#Ajout d'un client
def ajout_client(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = UserForm()
    return render(request, 'comptes/ajout_client.html', {'form': form})
#Modifivation des informations d'un client
def modifier_client(request, username):
    user = get_object_or_404(Users, username=username)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('clients')
    else:
        form = UserForm(instance=user)
    return render(request, 'comptes/ajout_client.html', {'form':form, 'modifier': True})
#Suppression d'un client
def supprimer_client(request, username):
    user = get_object_or_404(Users, username=username)
    if request.method == 'POST':
        user.delete()
        return redirect('clients')
    return render(request, 'comptes/confirmer_suppression.html', {'user':user})
#Affichage du profil client
def profil(request):
    user = request.user
    return render(request, 'comptes/profil.html', {'user': user})
#Envoi d'un message
def contact(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        objet = request.POST.get('objet')
        message = request.POST.get('message')
        ContactMessage.objects.create(nom=nom,
                                      email=email,
                                      objet=objet,
                                      message=message)
        messages.success(request, "Votre message a été envoyé !")
        return redirect('contact')
    return render(request, 'contact.html')
#Détail du message
def detailmessage(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.lu:
        msg.lu = True
        msg.save()
    return render(request, 'comptes/detail_message.html', {'message': msg})
#Affichage du message
def message(request):
    message = ContactMessage.objects.all().order_by('-date_envoi')
    non_lus_count = ContactMessage.objects.filter(lu=False).count()
    return render(request, 'comptes/message.html', context={'message': message, 'non_lus_count': non_lus_count})

