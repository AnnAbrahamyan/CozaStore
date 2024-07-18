from django.urls import path
from .views import *


urlpatterns = [
    path('', paypal_home, name="paypalhome"),
    path('payment_done', payment_done, name="payment_done"),
    path('payment_cancelled', payment_canceled, name="payment_cancelled"),
]
