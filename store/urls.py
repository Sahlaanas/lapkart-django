from django.urls import path
from .  import views





urlpatterns = [
    path('', views.store, name = 'store'),
    path('store/<str:cat_slug>/<int:prod_id>/', views.productview, name = 'productview'),
  
    

    
   
    
    
    
    
    
]