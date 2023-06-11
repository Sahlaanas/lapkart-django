from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . models import Wishlist
from django.http import JsonResponse
from store.models import Product
from wishlist.models import Wishlist
from django.contrib import messages
# Create your views here.
@login_required(login_url='login')
def wishlist(request):
    wishlistitems = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlistitems' : wishlistitems,
        }
    return render(request, 'wishlist/wishlist.html', context)

import traceback




def addTowishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            prod_id = int(request.POST.get('product_id'))
            product_check = Product.objects.get(id=prod_id)
            
            if(product_check):
                if(Wishlist.objects.filter(user=request.user, product_id=prod_id)):
                    return JsonResponse({'status' : "Product already in wishlist"})
                else:
                    Wishlist.objects.create(user=request.user, product_id=prod_id)
                    return JsonResponse({'status' : "Product added to wishlist"})
            else:
                return JsonResponse({'status' : "No such product found"})
        else:
            return JsonResponse({'status' : "Login to continue"})
    return redirect('/')            
   
   
def remove_wishlist(request):
    if request.method == "POST":
        prod_id = request.POST.get('product_id')
        print(prod_id)
        
        if prod_id is not None:
            prod_id = int(prod_id)
            if Wishlist.objects.filter(product_id=prod_id).exists():
                wishitem = Wishlist.objects.get(product_id=prod_id)
                wishitem.delete()
                messages.success(request, "Item deleted successfully")
    return redirect('wishlist')
            
        
