from django.shortcuts import render, redirect
from django.http import HttpResponse
from useraccount.models import Account
from category.models import Category
from store.models import Brand
from .models import Banner
from store.models import Product
from django.contrib import messages
from cart.models import Profile,Cart,CartItem


# Create your views here.
def home(request):
    user = Account.objects.all()
    catogories = Category.objects.all()
    brands = Brand.objects.all()
    banners = Banner.objects.all()
    products = Product.objects.all()
    profile = Profile.objects.all()
    
    context = {
        'user': user,
        'brands' : brands,
        'banners' : banners,
        'categories' : catogories,
        'products' : products,
        'profile' : profile, 
    }
    
    
    return render(request, 'user_home/index.html', context)

def storeview(request,slug):
    if(Category.objects.filter(slug=slug)):
        product = Product.objects.filter(category__slug = slug)
        category_name = Category.objects.filter(slug=slug).first()
        context = {
            'product' : product,
            'category_name' : category_name,
            
        }
        return render(request, 'store/store.html', context)
    else:
        messages.warning(request, "No such category found")
        return redirect('home')

def bookservice(request):
    return render(request, 'dashboard/404.html')


# def error_404_view(request,exception):
#     return render(request,'dashboard/404.html')