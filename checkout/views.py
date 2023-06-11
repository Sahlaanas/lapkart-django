from django.shortcuts import render, redirect
from cart.models import Cart, CartItem,Coupon
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from useraccount.models import Account
from userprofile.models import User_Address
from . models import Order, Order_item, Payment_methods
from store.models import Product
import random
from django.http import JsonResponse,HttpResponseRedirect
import razorpay
from django.views.decorators.cache import cache_control
from order.models import Wallet




# Create your views here.

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def checkout(request):
    rawcart = CartItem.objects.filter(cart__user=request.user)
    cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()
    carts = Cart.objects.filter(user=request.user)
    
    # Remove cart items where product_quantity exceeds size_variant stock
    for item in rawcart:
        if item.size_variant and item.product_quantity > item.size_variant.stock:
            item.delete()
            
    cartitems = CartItem.objects.filter(cart__user=request.user)
    tax = 0
    subtotal = 0
    grandtotal = 0
    
    for item in cartitems:
        subtotal += item.get_product_subtotal()
        
    tax = subtotal * 0.18
   
    
    coupon = None
    
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        coupon_obj = Coupon.objects.filter(coupon_code__icontains=coupon_code).first()

        if not coupon_obj:
            messages.warning(request, "Invalid Coupon")
            return redirect('checkout')


        if cart_obj.coupon:
            messages.warning(request, "Coupon already applied")
            return redirect('checkout')

        if cart_obj.get_cart_total() < coupon_obj.minimum_amount:
            messages.warning(request, f'Amount should be greater than {coupon_obj.minimum_amount}')
            return redirect('checkout')

        if coupon_obj.is_expired:
            messages.warning(request, "Coupon expired")
            return redirect('checkout')

        cart_obj.coupon = coupon_obj
        cart_obj.save()

        coupon_obj.is_applied = True
        coupon_obj.save()

        messages.success(request, 'Coupon applied')
        return redirect('checkout')

    grandtotal=subtotal + tax + 70
        
            
        
        
    userprofile = User_Address.objects.filter(user=request.user).first()
    coupons = Coupon.objects.filter(is_applied=False, is_expired=False)
 
    
    
    context = {
        'cartitems': cartitems,
        'subtotal': subtotal,
        'grandtotal': grandtotal,
        'tax' : tax,
        'coupon' : coupon,
        'userprofile' : userprofile,
        'cart' : cart_obj,
        'carts' : carts,
        'coupons' : coupons
        
    }
    
    return render(request, 'checkout/checkout.html', context)

@cache_control(no_cache=True, must_revalidate=True,no_store=True)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def placeorder(request):
    if request.method == "POST":
        currentuser = Account.objects.filter(id=request.user.id).first()
        payment_mode_value = request.POST.get('payment_mode')
        payment_mod = Payment_methods.objects.get(method__icontains=payment_mode_value)
        userprofile = User_Address.objects.filter(user=request.user).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('fname')
            currentuser.last_name = request.POST.get('lname')
            currentuser.save()

        if not (request.POST.get('address') and request.POST.get('city') and request.POST.get('district') and request.POST.get('state') and request.POST.get('country') and request.POST.get('pincode')):
            # Display a message indicating that all address fields are required
            messages.error(request, "Please fill in all address fields before placing the order.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if not userprofile:
            userprofile = User_Address()
            userprofile.user = request.user
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.district = request.POST.get('district')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.district = request.POST.get('district')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')
        neworder.payment_mode = payment_mod
        neworder.payment_id = request.POST.get('payment_id')
  
        
        

        cartitems = CartItem.objects.filter(cart__user=request.user)
        cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()
        tax = 0
        subtotal = 0
        grandtotal = 0

        for item in cartitems:
            subtotal += item.get_product_subtotal()

        tax = subtotal * 0.18

        grandtotal = subtotal + tax + 50
        neworder.total_price = grandtotal
        
        if (payment_mod.method == "Wallet"):
            wallet = Wallet.objects.get(user = request.user)
            
            
            if wallet.wallet >= grandtotal:
                wallet.wallet = wallet.wallet-grandtotal
                wallet.save()
            else:
                messages.error(request,'Your wallet amount is very low')
                return redirect('checkout')
        
        

        if cart_obj:
            trackno = 'LapK' + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno) is None:
                trackno = 'LapK' + str(random.randint(1111111, 9999999))

            neworder.tracking_no = trackno
            neworder.save()

            neworderitems = CartItem.objects.filter(cart__user=request.user)

            for item in neworderitems:
                Order_item.objects.create(
                    order=neworder,
                    product=item.product,
                    price=item.get_product_price(),
                    quantity=item.product_quantity,
                )

                if item.size_variant:
                    item.size_variant.stock -= item.product_quantity
                    item.size_variant.save()

            # To clear cart
            Cart.objects.filter(user=request.user).delete()
            
          

            payMode = request.POST.get('payment_mode')
            if payMode == "Razorpay":
                return JsonResponse({'status': "Your order has been placed"})
            else:
                messages.success(request, "Your order has been placed successfully")

    return render(request, 'checkout/checkout.html')



def razorpaycheck(request):
    cart = CartItem.objects.filter(cart__user=request.user)
    cart_obj = Cart.objects.get(is_paid = False, user=request.user)
    tax = 0
    subtotal = 0
    grandtotal = 0
    
    for item in cart:
        subtotal += item.get_product_subtotal()
        
    tax = subtotal * 0.18
    grandtotal=cart_obj.get_cart_total() + tax + 50  


            
    return JsonResponse({
        'total_price' : grandtotal
    })
    
    
