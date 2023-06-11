from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.signin, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('forgetpassword/', views.forgetpassword, name = 'forgetpassword'),
    path('resetpassword/', views.resetpassword, name = 'resetpassword'),
    path('product-list/', views.productlist, name='product_list'),
    path('searchproduct/', views.searchproduct, name = 'searchproduct'),
    
    
] 
