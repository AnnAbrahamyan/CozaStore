from paypal.standard.models import ST_PP_COMPLETED, ST_PP_FAILED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from main.models import Cart
from django.dispatch import receiver

@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == "Completed":
        Cart.objects.create()

@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_FAILED:
        Cart.objects.create()