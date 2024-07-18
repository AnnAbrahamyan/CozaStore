from django.contrib import admin
from django.urls import path, include,  re_path
from django.conf.urls.static import static
from django.conf import settings
from .handlers import custom_page_not_found_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('paypal/', include('paypal_payment.urls')),
    path('paypal-payment/', include('paypal.standard.ipn.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns +=  [
        re_path(r'^.*$', custom_page_not_found_view, {'exception': Exception('Page not Found')}),
    ]