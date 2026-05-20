from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Django Admin Panel
    path('admin/', admin.site.urls), 
    
    # 2. Django Built-in Auth (Handles /accounts/login/ and /accounts/logout/)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # 3. Your App URLs (Home, Product List, Details)
    path('', include('products.urls')),
]

# 4. Media and Static files configuration for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)