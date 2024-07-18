from django.contrib import admin, messages
from django.utils.html import format_html
from .models import (
    Product, Image, Size, Color, Quantity,
    ClothingOwnerDetector, ClothingType, Review,
    ContactSubmission, LikedProduct, Cart,
    ShippingInformation
)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        sizes = form.cleaned_data.get('size')
        quantities = form.cleaned_data.get('quantity')
        
        try:
            if sizes and quantities:
                if sizes.count() != quantities.count():
                    messages.warning(request, "Number of items in size must match the number of items in quantity. Changes were not saved.")
                    return 
        
            super().save_model(request, obj, form, change)
        
        except ValueError as e:
            messages.warning(request, f"An error occurred: {str(e)}")

    list_display = ['image_previews', 'id', 'material', 'owner_detector', 'price', 'updated_at', 'created_at']
    list_display_links = ['image_previews', 'id', 'material', 'owner_detector', 'price', 'updated_at', 'created_at']

    def image_previews(self, obj):
        images = obj.img.first()  
        if images:
            return format_html('<img src="{}" style="height: 50px; margin-right: 10px;"/>', images.img.url)
        return ""
    
    image_previews.short_description = 'Images'
    image_previews.allow_tags = True


@admin.register(Image)
class ImageModelAdmin(admin.ModelAdmin):
    list_display = ['image_previews']
    list_display_links = ['image_previews']

    def image_previews(self, obj):
        images = obj.img.first()  
        if images:
            return format_html('<img src="{}" style="height: 50px; margin-right: 10px;"/>', images.img.url)
        return ""

admin.site.register(Size)
admin.site.register(Color)
admin.site.register(Quantity)
admin.site.register(ClothingOwnerDetector)
admin.site.register(ClothingType)
admin.site.register(Review)
admin.site.register(ContactSubmission)
admin.site.register(LikedProduct)
admin.site.register(Cart)
admin.site.register(ShippingInformation)

