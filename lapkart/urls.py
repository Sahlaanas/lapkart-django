"""
URL configuration for lapkart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('login/', include('useraccount.urls')),
    path('store/', include('store.urls')),
    path('cart/', include('cart.urls')),
    path('dashboard/', include('dashboard_home.urls')),
    path('brandlist/', include('dashboard.urls')),
    path('adminprofile/', include('dashboard_users.urls')),
    path('userprofile/', include('userprofile.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('checkout/', include('checkout.urls')),
    path('myorders/', include('order.urls')),
    path('productlist/',include('admin_product.urls')),
    path('bannerlist/', include('admin_banner.urls')),
    path('orderlist/', include('admin_order.urls')),
    path('offerlist/', include('admin_offer.urls')),
    
    
    
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


