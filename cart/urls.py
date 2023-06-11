from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.cart, name = 'cart'),
    path('add-to-cart/<int:prod_id>/', views.add_to_cart, name = 'add_to_cart'),
    path('deleteCartItem/', views.remove_cart, name = 'remove_cart'),
    path('updateCart/', views.updateCart, name = 'updateCart'),
    
    
] 
