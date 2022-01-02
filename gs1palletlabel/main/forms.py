from .models import Labels
from django.forms import ModelForm, TextInput, NumberInput, Textarea


class LabelForm(ModelForm):
    class Meta:
        model = Labels
        fields = ["order_number", "supplier_id", "destination_id", "pallets_count", "product_id", "link_to_pdf"]
        widgets = {
            "order_number": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numaru Comenzii'
            }),
            "supplier_id": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'supplier_id',
            }),
            "destination_id": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'destination_id',
            }),
            "pallets_count": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'pallets_count',
            }),
            "product_id": NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'product_id',
            }),
            "link_to_pdf": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'link_to_pdf'
            }),

        }