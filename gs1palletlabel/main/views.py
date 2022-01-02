from django.shortcuts import render, redirect
from .models import Labels, Suppliers
from .forms import LabelForm


def index(request):
    labels = Labels.objects.order_by('id')
    supplier_id = Suppliers.objects.all()
    return render(request, 'main/index.html', {'title':'Pagina Principala', 'labels':labels,'supplier_id':supplier_id})


def about(request):
    return render(request, 'main/about.html', {'title':'Pagina despre Site'})


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
