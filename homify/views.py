from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import render, redirect

from homify.models import Houses, Onsale, Client


# Create your views here.
def home(request):
    return render(request, 'home.html')


def houses_on_sale(request):
    houses = Houses.objects.all()
    return render(request, 'houses_on_sale.html', {"houses": houses})


def purchased_houses(request):
    purchased = Onsale.objects.all()
    return render(request, 'purchased_houses.html', {"purchased": purchased})


def houses(request):
    return render(request, 'houses.html')


def purchase_house(request, id):
    house = Houses.objects.get(id=id)
    clients = Client.objects.all()
    if request.method == 'POST':
        client_id = request.POST['client_id']
        client = Client.objects.get(id=client_id)
        deadline_of_payment = date.today() + timedelta(days=200)
        onsale = Onsale.objects.create(house=house, customer=client, deadline_of_payment=deadline_of_payment, status='PURCHASED')
        onsale.save()
        messages.success(request,  f"The house, {house.name} has been purchased successfully")
        return redirect('houses')

    return render(request, 'purchase.html', {"house": house, "clients": clients})


def refund(request, id):
    onsale = Onsale.objects.get(id=id)
    onsale.return_date = date.today()
    onsale.status = 'REFUNDED'
    onsale.save()
    messages.success(request, f"Payment for {onsale.house.name} refunded successfully")
    return redirect('houses')


def interest_accrued(request):
    onsale = Onsale.objects.all()
    fines = [t for t in onsale if t.total_fine > 0]
    return render(request, 'fines.html', {"fines": fines})


def pay_overdue(request):
    onsale = Onsale.objects.get(pk=id)
    total = onsale.total_fine
    phone = onsale.client.phone
    return redirect('houses')