from django.shortcuts import render
from store.models import Product, screenSizeVariant
from . models import Cart, CartItem
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib import messages
from django.db.models import F
from django.shortcuts import get_object_or_404


def add_to_cart(request, prod_id):
    if request.user.is_authenticated:
        variant = request.GET.get('variant')
        quantity = int(request.GET.get('quantity'))
        product = get_object_or_404(Product, id=prod_id)
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

        if variant:
            size_variant = get_object_or_404(screenSizeVariant, size_name=variant)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, size_variant=size_variant)
        else:
            messages.error(request, "Select a size")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if created:
            # New cart item created
            if variant and size_variant.stock < quantity:
                messages.error(request, "Not enough stock available for the selected variant.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            cart_item.product_quantity = quantity
        else:
            # Existing cart item updated
            new_quantity = cart_item.product_quantity + quantity

            if variant and size_variant.stock < new_quantity:
                messages.error(request, "Not enough stock available for the selected variant.")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            cart_item.product_quantity = new_quantity

        # Check if the product is already in the cart
        if created:
            messages.success(request, "Product added to cart")
        else:
            messages.error(request, "Product is already in the cart")

        cart_item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, "Please login to continue")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


from django.shortcuts import render, redirect
def remove_cart(request):
    if request.method == "POST":
        print(request.POST)  # Debugging statement
        prod_id = request.POST.get('product_id')
        print(prod_id)  # Debugging statement

        if prod_id is not None:
            prod_id = int(prod_id)
            cart_items = CartItem.objects.filter(cart__user=request.user, product_id=prod_id)
            if cart_items.exists():
                cart_items.delete()
                messages.success(request, "Item deleted successfully.")
    return redirect('cart')



    
    
def cart(request):
    cart = Cart.objects.filter(is_paid = False, user = request.user)
    cartitem = CartItem.objects.filter(cart__is_paid = False, cart__user = request.user)
    tax = 0
    subtotal = 0
    grandtotal = 0
    for item in cartitem:
        subtotal+= item.get_product_subtotal()
    tax= subtotal*0.18
    grandtotal = subtotal+tax+70
    
    context = {
        'cart' : cart,
        'cartitem' : cartitem,  
        'subtotal' : subtotal, 
        'tax' : tax, 
        'grandtotal' : grandtotal,
    }
    
    return render(request, 'cart/cart.html', context)

from django.core.exceptions import ObjectDoesNotExist

def updateCart(request): 
    if request.method == "POST":
        prod_id = int(request.POST.get('product_id'))
        try:
            cart = CartItem.objects.get(product_id=prod_id, cart__user=request.user)
            prod_qty = int(request.POST.get('product_qty'))
            cart.product_quantity = prod_qty
            cart.save()
            
            subtotal = 0
            for item in CartItem.objects.filter(cart__user=request.user):
                subtotal += item.get_product_subtotal()
            
            return JsonResponse({
                'status': "Updated Successfully",
                'product_price': cart.get_product_price(),
                'quantity': cart.product_quantity,
                'subtotal': subtotal
            })
        except ObjectDoesNotExist:
            pass
        
    return render(request, 'cart/cart.html')

    
    