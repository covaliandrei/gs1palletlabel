from .models import Labels, Suppliers, Destinations, Products
from django.forms import ModelForm, TextInput, NumberInput, Select, HiddenInput


class LabelForm(ModelForm):
    class Meta:
        model = Labels
        supplier_id = list(Suppliers.objects.all().values())
        destination_id = list(Destinations.objects.all().values())
        product_id = list(Products.objects.all().values())

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
            }),
            "product_id": Select(attrs={
                'class': 'form-control',
                'data-list': product_id,
            }),
            "link_to_pdf": HiddenInput(attrs={
                'value': '#'
            }),

        }
