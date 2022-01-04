from django.forms import ModelForm, TextInput, NumberInput, Select, HiddenInput, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from django import forms
from .models import Labels, Suppliers, Destinations, Products


class LabelForm(ModelForm):
    class Meta:
        model = Labels
        supplier_id = list(Suppliers.objects.all().values())
        destination_id = list(Destinations.objects.all().values())
        product_id = list(Products.objects.all().values())
        print(destination_id)
        fields = ["order_number", "supplier_id", "destination_id", "pallets_count", "product_id", "link_to_pdf"]
        widgets = {
            "order_number": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numaru Comenzii'
            }),
            "supplier_id": Select(attrs={
                'class': 'form-control',
                'data-list': supplier_id,
            }),
            "destination_id": Select(attrs={
                'class': 'form-control',
                'data-list': destination_id,
            }),
            "pallets_count": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantitatea paletelor',
                'value': 1
            }),
            "product_id": Select(attrs={
                'class': 'form-control',
                'data-list': product_id,
            }),
            "link_to_pdf": HiddenInput(attrs={
                'value': '#'
            }),

        }


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            "username": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nume Utilizator',
            }),
            "email": EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'E-Mail Utilizator',
            }),
            "password1": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Parola',
            }),
            "password2": PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirma Parola',
            })

        }
