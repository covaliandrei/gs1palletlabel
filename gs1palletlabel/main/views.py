from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import os
import treepoem
from fpdf import FPDF

from django.contrib.auth.decorators import login_required

# from django.contrib.auth.models import User

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

            order_number = '3831 30122101'
            supplier_name = 'Cuptor Production S.R.L.'
            destination_name = 'LIDL Iernut, Strada Campului nr. 3, 545100 Iernut '
            product_name = 'Invirtita cu umplutura de prune si nuci,semifabricat,congelat,60buc x165g'
            product_scu = '4842076003136'
            boxes_per_pallet = '80'
            weight_brutto = '845,000'
            weight_netto = '792,000'
            pallets_count = 3

            prod = list(Products.objects.all().filter(id=int(request.POST['product_id']
                                                             )
                                             ).values('product_scu', 'boxes_per_pallet', 'weight_brutto', 'weight_netto')
            )

            label = PdfLabel(
                request.POST['order_number'],
                str(list(Suppliers.objects.filter(id=int(request.POST['supplier_id'])))[0]),
                str(list(Destinations.objects.filter(id=int(request.POST['destination_id'])))[0]),
                str(list(Products.objects.filter(id=int(request.POST['product_id'])))[0]),
                prod[0]['product_scu'],
                str(prod[0]['boxes_per_pallet']),
                prod[0]['weight_brutto'],
                prod[0]['weight_netto'],
                int(request.POST['pallets_count']))

#            print(prod[0]['product_scu'])

#            print(request.POST['supplier_id'])
#            print(request.POST['destination_id'])
#            print(request.POST['product_id'])
#            print(request.POST)

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


@login_required(login_url='login')
def delete(request, pk):
    label = Labels.objects.get(id=pk)
    if request.method == "POST":
        label.delete()
        return redirect('/')

    context = {'item':label}
    return render(request, 'main/delete.html', context)


def gencode128(textdata):
    return treepoem.generate_barcode(
        barcode_type='code128',
        data=textdata,
         options={
            'width': '4',
            'height': '1',
        },
    )

def PdfLabel(order_number,
               supplier_name,
               destination_name,
               product_name,
               product_scu,
               boxes_per_pallet,
               weight_brutto,
               weight_netto,
               pallets_count):

    stringsz = [
            "GS1 LOGISTIC LABEL",
            "NUMARUL COMENZII",
            "FROM: ",
            "TO: ",
            "SORTIMENT",
            "CODUL SSCC",
            "NUMARUL DE CARTOANE DE PE PALET: ",
            "CANTITATEA BRUTA DE PE PALET: ",
            "CANTITATEA NETA DE PE PALET: ",
            "SSCC:"
        ]

    datas = [
            "",
            order_number,
            supplier_name,
            destination_name,
            product_name,
            product_scu,
            boxes_per_pallet,
            weight_brutto,
            weight_netto,
            "(00)"+product_scu
    ]

    if not os.path.exists('main\\images\\' + datas[8] + '.png'):
        image = gencode128(datas[8])
        image.convert('1').save('main\\images\\' + datas[8] + '.png')
    if not os.path.exists('main\\images\\' + datas[9] + '.png'):
       image = gencode128(datas[9])
       image.convert('1').save('main\\images\\' + datas[9] + '.png')

    pdf = FPDF('P', 'mm', 'A4')
    j = 1
    while j <= pallets_count:
        pdf.add_page("L")
        pdf.set_auto_page_break(True, 10)
        pdf.set_font("Arial", '', 10)
        pdf.set_top_margin(2)
        pdf.set_left_margin(2)
        pdf.set_right_margin(2)
        offset = 3
        i = 1
        while i <= 2:
            pdf.set_font('', '', 10)
            pdf.rect(offset + 3, 4, 141, 11)
            pdf.set_xy(offset + 3, 6)
            pdf.cell(0, 4, stringsz[0], 0, 1, "L", False)

            pdf.set_xy(offset + 23, 7)

            pdf.cell(0, 6, datas[0], 0, 1, "L", False)

            pdf.rect(offset + 3, 15, 141, 14)

            pdf.set_xy(offset + 3, 16)
            pdf.set_font('', '', 10)
            pdf.cell(0, 4, stringsz[2], 0, 1, "L", False)

            pdf.set_xy(offset + 30, 21)
            pdf.set_font('', 'B', 12)
            pdf.cell(0, 6, datas[2], 0, 1, "L", False)

            pdf.rect(offset + 3, 29, 141, 10)

            pdf.set_xy(offset + 3, 30)
            pdf.set_font('', '', 10)
            pdf.cell(0, 4, stringsz[3], 0, 1, "L", False)

            pdf.set_xy(offset + 30, 30)
            pdf.set_font('', 'B', 12)
            pdf.cell(0, 6, datas[3], 0, 1, "L", False)

            pdf.rect(offset + 3, 39, 141, 30)

            pdf.set_xy(offset + 28, 62)
            pdf.image('main\\images\\' + datas[8] + '.png', offset + 8, 42, 60, 20)
            pdf.cell(0, 6, datas[8], 0, 1, "L", False)

            pdf.rect(offset + 3, 69, 141, 60)
            pdf.set_xy(offset + 30, 71)
            pdf.set_font('', 'B', 12)
            pdf.cell(0, 6, 'PALET NR. ' + str(j), 0, 1, "L", False)
            pdf.set_xy(offset + 3, 76)
            pdf.set_font('', '', 10)
            pdf.cell(0, 4, stringsz[1] + ' :  ' + datas[1], 0, 1, "L", False)
            pdf.set_xy(offset + 3, 82)
            pdf.cell(0, 4, stringsz[4] + ' :  ' + datas[4], 0, 1, "L", False)
            pdf.set_xy(offset + 3, 88)
            pdf.cell(0, 4, stringsz[5] + ' :  ' + datas[5], 0, 1, "L", False)

            pdf.set_xy(offset + 3, 94)
            pdf.cell(0, 4, stringsz[6] + ' :  ' + datas[6], 0, 1, "L", False)

            pdf.set_xy(offset + 3, 100)
            pdf.cell(0, 4, stringsz[7] + ' :  ' + datas[7], 0, 1, "L", False)

            pdf.set_xy(offset + 3, 106)
            pdf.cell(0, 4, stringsz[8] + ' :  ' + datas[8], 0, 1, "L", False)

            pdf.rect(offset + 3, 129, 141, 46)
            pdf.set_xy(offset + 8, 132)
            pdf.set_font('', 'B', 12)
            pdf.cell(0, 4, 'SSCC :  ' + datas[5], 0, 1, "L", False)
            pdf.image('main\\images\\' + datas[9] + '.png', offset + 8, 138, 130, 26)
            pdf.set_xy(offset + 38, 166)
            pdf.set_font('', 'B', 18)
            pdf.cell(0, 4, datas[9], 0, 1, "L", False)
            offset = 146
            i += 1
        j += 1

    pdf.output('main\\labels\\' + order_number + '.pdf', 'F')
    return 'main\\labels\\' + order_number + '.pdf'



