from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.productlist, name = 'productlist'),
    path('createproduct/', views.createproduct, name = 'createproduct'),
    path('deleteproduct/<int:deleteproduct_id>/', views.deleteproduct, name='deleteproduct'),    
    path('editproduct/<int:editproduct_id>', views.editproduct, name='editproduct'),
    
    
    path('couponlist/', views.couponlist, name = 'couponlist'),
    path('addcoupon/', views.addcoupon, name = 'addcoupon'),
    path('deletecoupon/<int:deletecoupon_id>/', views.deletecoupon, name = 'deletecoupon'),
    path('editcoupon/<int:editcoupon_id>/', views.editcoupon, name='editcoupon'),
    
] 
 