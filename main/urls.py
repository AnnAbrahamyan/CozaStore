from django.urls import path
from .views import (
    HomeListView, LogInView, RegisterView,
    ForgotPasswordView, CustomLogoutView,
    ShopListView, ProductDetailView, add_review,
    contact_view, ContactUsView, like_product,
    AboutUsModel, Wishlist, add_to_cart,
    CartItemsView, update_cart_quantity,
    save_shipping_info
)

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('accounts/login/', LogInView.as_view(), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('shop/', ShopListView.as_view(), name='shop'),
    path('product-detail/<int:prod_id>/<int:prod_code>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-review/<int:prod_id>/', add_review, name='add_review'),
    path('contact/', ContactUsView.as_view(), name='contact'),
    path('contact-us/', contact_view, name='contact-us'),
    path('like/<int:product_id>/', like_product, name='like_product'),
    path('about/', AboutUsModel.as_view(), name='about'),
    path('wishlist/', Wishlist.as_view(), name='wishlist'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('cart-items/', CartItemsView.as_view(), name='cart-items'),
    path('update-cart-quantity/', update_cart_quantity, name='update_cart_quantity'),  
    path('save-shipping-info/', save_shipping_info, name='save_shipping_info'),
]
