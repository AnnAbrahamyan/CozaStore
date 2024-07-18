from main.models import LikedProduct, Cart

def liked_product_count(request):
    if request.user.is_authenticated:
        liked_product_count = LikedProduct.objects.filter(user=request.user).count()
    else:
        liked_product_count = 0
    
    return {'liked_product_count': liked_product_count}


def cart_product_count(request):
    if request.user.is_authenticated:
        cart_product_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_product_count = 0
    
    return {'cart_product_count': cart_product_count}