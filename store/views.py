from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,screenSizeVariant
from category.models import Category
from django.contrib import messages
from django.http import HttpResponse
from .models import Brand,price_filter
from django.db.models import F
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


# Create your views here.
def store(request):
    
    # products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    filter_prices = price_filter.objects.all()
    product = Product.objects.all()
    
    product_count = product.count()
    Cat_id = request.GET.get('categories')
    filter_price_id = request.GET.get('filter_price')
    brand_id = request.GET.get('brand')
    sort = request.GET.get('sort')
    search_query = request.GET.get('search_query')
    

    
    
    
    if search_query:
        product = Product.objects.filter(product_name__icontains=search_query)
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        


    elif Cat_id:
        product = Product.objects.filter(category__id=Cat_id)
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
    elif filter_price_id:
        product = Product.objects.filter(filt_price=filter_price_id)
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
    elif brand_id:
        product = Product.objects.filter(brand__id=brand_id)
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
    elif sort == 'atoz':
        product = Product.objects.order_by('product_name')
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
        
    elif sort == 'ztoa':
        product = Product.objects.order_by('-product_name')
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
    elif sort == 'ltoh':
        product = Product.objects.order_by('price')
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        
    elif sort == 'htol':
        product = Product.objects.order_by(F('price').desc())
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
               
    else:
        product = Product.objects.all()
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        paged_product = paginator.get_page(page)
        p_count = product.count()
        

        
    context = {
        # 'products' : products,
        'categories' : categories,
        'brands' : brands,
        'filter_prices' : filter_prices,
        'product' : paged_product,
        'product_count' : product_count,
        'search_query': search_query,
        'p_count' : p_count,
       
    }
    for category in categories:
        product_count = category.product_set.count()
        category.product_count = product_count
    
    return render(request, 'store/store.html', context)



def productview(request, cat_slug, prod_id):
    if Category.objects.filter(slug=cat_slug).exists():
        if Product.objects.filter(identification=prod_id).exists():
            product = Product.objects.filter(identification=prod_id).first
            
            context = {
                'product' : product,
                
            }
            
            if request.GET.get('size'):
                size = request.GET.get('size')
                product = Product.objects.get(identification=prod_id)
                price = product.price + screenSizeVariant.objects.get(size_name = size).price
                context['selected_size'] = size
                context['updated_price'] = price
                
                
            if request.GET.get('quantity'):
                qty = request.GET.get('quantity')
                context['qnty'] = qty
                print('ttttttttttttttttttttttttt', qty)
                

        else:
            messages.error(request, "No such products found") 
            return redirect('store')
    else:
        messages.error(request, "No such category found")
        return redirect('store')
    return render(request, 'store/productview.html', context=context)

