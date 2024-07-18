from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, View
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Sum
from .models import (
    Product, Color, Review, LikedProduct,
    Cart, Size, LikedProduct, ShippingInformation
)
from .forms import ContactForm


User = get_user_model()


class HomeListView(ListView):
    model = Product
    template_name = 'main/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.all()
        sort_by = self.request.GET.get('sort_by')
        price = self.request.GET.get('price')
        color = self.request.GET.get('color')

        if price:
            if price == '0-50':
                queryset = queryset.filter(price__lte=50)
            elif price == '50-100':
                queryset = queryset.filter(price__gt=50, price__lte=100)
            elif price == '100-150':
                queryset = queryset.filter(price__gt=100, price__lte=150)
            elif price == '150-200':
                queryset = queryset.filter(price__gt=150, price__lte=200)
            elif price == '200+':
                queryset = queryset.filter(price__gt=200)

        if color:
            queryset = queryset.filter(color__color=color)

        queryset = queryset.annotate(avg_rating=Avg('review__rating'))

        if sort_by:
            if sort_by == 'rating':
                queryset = queryset.order_by('-avg_rating')
            elif sort_by == 'price_low_high':
                queryset = queryset.order_by('price')
            elif sort_by == 'price_high_low':
                queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()

        if self.request.user.is_authenticated:
            liked_product_ids = LikedProduct.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            context['liked_product_ids'] = list(liked_product_ids)
        else:
            context['liked_product_ids'] = []

        return context



class LogInView(View):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid email or password. Please try again.'
            return render(request, self.template_name, {'error': error_message, 'barev': 'barevhazarbarin'})
    

class RegisterView(ListView):
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('home')  
            except IntegrityError as e:
                form.add_error('email', 'This email is already taken.')
        return render(request, self.template_name, {'form': form})
    



class ForgotPasswordView(ListView):
    template_name = 'registration/forgot_password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        if email:
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    token = default_token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    reset_link = request.build_absolute_uri(
                        reverse_lazy('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                    )
                    subject = 'Password Reset Requested'
                    context = {
                        'user': user,
                        'reset_link': reset_link,
                        'site_name': 'Your Site Name'  # Replace with your site name
                    }
                    html_content = render_to_string('main/password_reset_email.html', context)
                    text_content = 'You\'re receiving this email because you requested a password reset for your user account at {}.\n\nPlease go to the following page and choose a new password:\n\n{}\n\nYour username, in case you\'ve forgotten: {}\n\nThanks for using our site!\n\nThe {} team'.format('Your Site Name', reset_link, user.get_username(), 'Your Site Name')
                    
                    email_message = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
                    email_message.attach_alternative(html_content, "text/html")
                    email_message.send()
                messages.success(request, 'Password reset link has been sent to your email.')
                return redirect('login')
            else:
                messages.error(request, 'No user is associated with this email.')
        return render(request, self.template_name)

    
    

class CustomLogoutView(ListView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('home'))
    



class ShopListView(ListView):
    model = Product
    template_name = 'main/product.html'
    context_object_name = 'products'
    paginate_by = 12  

    def get_queryset(self):
        queryset = Product.objects.all()
        sort_by = self.request.GET.get('sort_by')
        price = self.request.GET.get('price')
        color = self.request.GET.get('color')
        type = self.request.GET.get('type')
        search_query = self.request.GET.get('search')

        if search_query:
            normalized_query = search_query.lower().strip()

            queryset = queryset.filter(
                Q(product_name__icontains=normalized_query) |
                Q(description__icontains=normalized_query) |
                Q(material__icontains=normalized_query) |
                Q(owner_detector__owner_detector__icontains=normalized_query) |
                Q(size__size__icontains=normalized_query) |
                Q(color__color__icontains=normalized_query) |
                Q(type__type__icontains=normalized_query)
            )

        if price:
            if price == '0-50':
                queryset = queryset.filter(price__lte=50)
            elif price == '50-100':
                queryset = queryset.filter(price__gt=50, price__lte=100)
            elif price == '100-150':
                queryset = queryset.filter(price__gt=100, price__lte=150)
            elif price == '150-200':
                queryset = queryset.filter(price__gt=150, price__lte=200)
            elif price == '200+':
                queryset = queryset.filter(price__gt=200)

        if color:
            queryset = queryset.filter(color__color__icontains=color)

        if type:
            queryset = queryset.filter(type__type__icontains=type)

        queryset = queryset.annotate(avg_rating=Avg('review__rating'))

        if sort_by:
            if sort_by == 'rating':
                queryset = queryset.order_by('-avg_rating')
            elif sort_by == 'price_low_high':
                queryset = queryset.order_by('price')
            elif sort_by == 'price_high_low':
                queryset = queryset.order_by('-price')

        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colors'] = Color.objects.all()
        context['nav'] = 'shop'

        if self.request.user.is_authenticated:
            liked_product_ids = LikedProduct.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            context['liked_product_ids'] = list(liked_product_ids)
        else:
            context['liked_product_ids'] = []

        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    


class ProductDetailView(ListView):
    template_name = 'main/product-detail.html'

    def get(self, request: HttpRequest, prod_id, prod_code, *args: Any, **kwargs: Any) -> HttpResponse:
        single_product = get_object_or_404(Product, pk=prod_id)
        products_with_same_code = Product.objects.filter(code=prod_code)
        reviews = Review.objects.filter(product=prod_id)
        products = Product.objects.all()[:8]

        context = {
            'product': single_product,
            'products_with_same_code': products_with_same_code,
            'reviews': reviews,
            'products': products,
        }

        if self.request.user.is_authenticated:
            liked_product_ids = LikedProduct.objects.filter(user=self.request.user).values_list('product_id', flat=True)
            context['liked_product_ids'] = list(liked_product_ids)
        else:
            context['liked_product_ids'] = []

        return render(request, self.template_name, context)
    

@login_required
def add_review(request, prod_id):
    product = Product.objects.get(id=prod_id)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        if request.user.is_authenticated:
            user = request.user
            
            review = Review.objects.create(
                user=user,
                product=product,
                rating=rating,
                review_text=review_text
            )
            
            return redirect('product_detail', prod_id=product.id, prod_code=product.code) 
    
    return render(request, 'your_template.html', {'product': product})


class ContactUsView(ListView):
    template_name = 'main/contact.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = {
            'nav': 'contact',
        }

        return render(request, self.template_name, context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_submission = form.save()

            subject = 'Thank you for contacting us'
            message = 'We have received your message and will get back to you shortly.'
            recipient_list = [contact_submission.email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, fail_silently=False)

            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})




@login_required
def like_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    liked, created = LikedProduct.objects.get_or_create(user=request.user, product=product)
    if not created:
        liked.delete()
        return JsonResponse({'status': 'unliked'})
    return JsonResponse({'status': 'liked'})



class AboutUsModel(ListView):
    template_name = 'main/about.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        context = {
            'nav': 'about',
        }

        return render(request, self.template_name, context)
    

class Wishlist(ListView):
    template_name = 'main/wishlist.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        products = LikedProduct.objects.filter(user = request.user)[::-1]

        context = {
            'products': products,
        }

        return render(request, self.template_name, context)




@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        size_id = request.POST.get('size')
        color_id = request.POST.get('color')
        quantity = int(request.POST.get('quantity', 1))  

        product = get_object_or_404(Product, id=product_id)
        size = get_object_or_404(Size, id=size_id)
        color = get_object_or_404(Color, id=color_id)

        try:
            if quantity is None:
                quantity = 1

            total_price = product.price * quantity

            cart_item, created = Cart.objects.get_or_create(
                user=request.user,
                product=product,
                size=size,
                color=color,
                defaults={
                    'quantity': quantity,
                    'total_price': total_price
                }  
            )

            if not created:
                cart_item.quantity += quantity  
                cart_item.save()

            messages.success(request, 'Item added to cart successfully.')

            return redirect(reverse('product_detail', args=[product_id, product.code]))

        except IntegrityError as e:
            print(f"IntegrityError occurred: {e}")
            messages.error(request, 'Failed to add item to cart. Please try again later.')

    return redirect(reverse('product_detail', args=[product_id, product.code]))



class CartItemsView(ListView):
    model = Cart
    template_name = 'main/shoping-cart.html'
    context_object_name = 'products'  

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total_sum = context['products'].aggregate(total_sum=Sum('total_price'))['total_sum']
        total_sum = total_sum if total_sum else 0

        if total_sum < 100:
            total = total_sum + 10
        else:
            total = total_sum

        context['total_sum'] = f'{total_sum:.2f}'
        context['total'] = f'{total:.2f}'
        return context
    


@csrf_exempt
@require_POST
def update_cart_quantity(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    print(f"Received request to update product ID {product_id} to quantity {quantity}")  # Debugging line

    if quantity < 1:
        return JsonResponse({'success': False, 'error': 'Quantity must be at least 1'})

    try:
        cart_item = Cart.objects.get(id=product_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.total_price = cart_item.product.price * quantity
        cart_item.save()
        return JsonResponse({'success': True})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found in cart'})
    


@require_POST
def save_shipping_info(request):
    data = json.loads(request.body)
    shipping_info = data.get('shipping_info')
    country = data.get('country')
    state = data.get('state')
    zip_code = data.get('zip')
    
    # Save shipping information to the database
    shipping_info_model = ShippingInformation.objects.create(
        shipping_info=shipping_info,
        country=country,
        state=state,
        zip_code=zip_code
    )
    
    # Optionally, you can return a response indicating success
    return JsonResponse({'message': 'Shipping information saved successfully.'})








