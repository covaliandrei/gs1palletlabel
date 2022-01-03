from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User

from .models import Labels, Suppliers
from .models import *
from .forms import LabelForm, CreateUserForm


# def login(request):
#    context = {
#        'title': 'Autentificarea in sistem',
#   }
#    return render(request, 'main/login.html', context)


def register(request):
    # form = CreateUserForm()
    context = {}
    error = ''
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('login')
        else:
            error = 'Date eronate'

    form = CreateUserForm()
    context = {
        'form': form,
        'title': 'Inregistrarea in sistem',
        'error': error,
    }

    return render(request, 'main/register.html', context)


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def index(request):
    labels = Labels.objects.order_by('id')
    supplier_id = Suppliers.objects.all()
    return render(request, 'main/index.html', {'title':'Pagina Principala', 'labels':labels,'supplier_id':supplier_id})

@login_required(login_url='login')
def about(request):
    return render(request, 'main/about.html', {'title':'Pagina despre Site'})

@login_required(login_url='login')
def create(request):
    error = ''
    if request.method == 'POST':
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Date eronate'

    form = LabelForm()
    context = {
        'form': form,
        'title': 'Creaza Eticheta',
        'error': error,
    }
    return render(request, 'main/create.html',  context)
