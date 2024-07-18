from django.db import models
from django.contrib.auth.models import User

class PaypalOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.TextField()
    invoice_id = models.CharField(max_length=50, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.invoice_id} by {self.user.username}"
