from django.contrib import admin
from . models import Cart, CartItem, Profile,Coupon

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Profile)
admin.site.register(Coupon)

