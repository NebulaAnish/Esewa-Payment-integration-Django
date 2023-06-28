from django.shortcuts import render, redirect, get_object_or_404
from django.http import request
from .models import Order
import requests
import xmltodict

# Create your views here.

def orders_list(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    template = 'payment/orders.html'
    return render(request, template, context)

def order_checkout(request, id):
    order = Order.objects.get(id=id)
    context = {'order':order}
    template = 'payment/order_checkout.html'
    return render(request, template, context)


# For esewa callback

def esewa_callback_view(request):
    oid = request.GET.get('oid')
    amt = request.GET.get('amt')
    refId = request.GET.get('refID')
    url = "https://uat.esewa.com.np/epay/transrec"

    data = {
        'amt':amt,
        'sct' : 'EPAYTEST',
        'rid' : refId,
        'pid' : oid,
    }
    response = requests.post(url, data=data)
    json_response = xmltodict.parse(response.content)
    status = json_response["response"]["response_code"]

    if status != "Success":
        return redirect("payment_failed")
    order = get_object_or_404(Order, order_id=oid)

    if order.total_price != int(amt):
        return redirect("payment_failed")
    # In production environment, save amt in paisa while saving in database

    order.is_paid = True
    order.paid_amount = int(float(amt))
    order.save()
    return render(request, 'payment/esewa-callback.html')

def payment_failed(request):
    return render(request, 'payment/payment_failed.html')
