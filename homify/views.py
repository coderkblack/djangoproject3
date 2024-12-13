import json
from datetime import date, timedelta

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient

from homify.models import Houses, Onsale, Client, Payment


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


def pay_overdue(request, id):
    onsale = Onsale.objects.get(pk=id)
    total = onsale.total_fine
    phone = onsale.customer.phone
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0791736258'
    amount = 1
    account_reference = '002-ABC'
    transaction_desc = 'Fines'
    callback_url = 'https://sparrow-hip-flamingo.ngrok-free.app/callback'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    if response.response_code == "0":
        payment = Payment.objects.create(onsale=onsale, merchant_request_id=response.merchant_request_id,
                                         checkout_request_id=response.checkout_request_id, amount=amount)
        payment.save()
        messages.success(request, f"Your payment was triggered successfully")
    return redirect('houses')

@csrf_exempt
def callbacks(request):
    resp = json.loads(request.body)
    data = resp['Body']['stkCallback']
    if data["ResultCode"] == "0":
        m_id = data["MerchantRequestID"]
        c_id = data["CheckoutRequestID"]
        code = ""
        item = data["CallbackMetadata"]["Item"]
        for i in item:
            name = i["Name"]
            if name == "MpesaReceiptNumber":
                code = i["value"]
        onsale = Onsale.objects.get(merchant_request_id=m_id, checkout_request_id=c_id)
        onsale.code = code
        onsale.status = "COMPLETED"
        onsale.save()
    return HttpResponse("OK")