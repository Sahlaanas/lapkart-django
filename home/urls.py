from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.home, name = 'home'),
    path('storeview/<str:slug>/', views.storeview, name = 'storeview'),
    path('bookservice/', views.bookservice,name='bookservice')
     
    
] 
