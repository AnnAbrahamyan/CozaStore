from django.urls import reverse
from django.shortcuts import render, redirect
from paypal.standard.forms import PayPalPaymentsForm
from CozaStore.settings import PAYPAL_RECEIVER_EMAIL
import uuid
from django.contrib import messages
from main.models import *
from datetime import datetime
from .models import PaypalOrder

def paypal_home(request):
    carts = Cart.objects.filter(user=request.user)
    
    item_names = []
    for item in carts:
        item.total_price = round(item.product.price * item.quantity, 2)
        item_names.append(f"{item.product.product_name} (x{item.quantity})")
            
    subtotal = round(sum([float(item.total_price) for item in carts]), 2)
    tax = round(subtotal * 0.1, 2)
    total = round(subtotal + tax, 2)
    
    item_name = ", ".join(item_names)
    
    invoice_id = f"INV-{request.user.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    host = request.get_host()
    paypal_dict = {
        "business": PAYPAL_RECEIVER_EMAIL,
        "amount": total,
        "item_name": item_name,
        "invoice": invoice_id,
        "currency_code": "USD",
        "notify_url": 'http://{}{}'.format(host, reverse("paypal-ipn")),
        "return": 'http://{}{}'.format(host, reverse('payment_done')),
        "cancel_return": 'http://{}{}'.format(host,reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "paypalpayment.html", context)



def payment_done(request):
    carts = Cart.objects.filter(user=request.user)
    item_names = []
    for item in carts:
        item.total_price = round(item.product.price * item.quantity, 2)
        item_names.append(f"{item.product.product_name} (x{item.quantity})")
            
    subtotal = round(sum([float(item.total_price) for item in carts]), 2)
    tax = round(subtotal * 0.1, 2)
    total = round(subtotal + tax, 2)
    
    item_name = ", ".join(item_names)
    
    invoice_id = f"INV-{request.user.id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    host = request.get_host()
    order = PaypalOrder.objects.create(
        user=request.user,
        item_name=item_name,
        invoice_id=invoice_id,
        total=total,
    )
    order.save()
    carts.delete()
    
    messages.success(request, "Payment succsessfully done")
    return redirect("paypalhome")

def payment_canceled(request):
    messages.error(request, "Something gone wrong: Payment declined")
    return redirect("paypalhome")

