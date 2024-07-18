from django.contrib import admin
from .models import PaypalOrder

@admin.register(PaypalOrder)
class PaypalOrderAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'user', 'item_name', 'total', 'created_at')
    search_fields = ('invoice_id', 'user__username', 'item_name')
    list_filter = ('created_at',)
