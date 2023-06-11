from django.db import models
from useraccount.models import Account
from store.models import Product, screenSizeVariant, RAMVariant


# Create your models here.

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    is_expired = models.BooleanField(default=False)
    discount_price = models.PositiveIntegerField(default=100)
    minimum_amount = models.PositiveIntegerField(default=500)
    is_applied = models.BooleanField(default=False)
    
    def __str__(self):
        return self.coupon_code
     
class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='photos/profile')
    


class Cart(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='carts')
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL, null=True, blank = True)
    is_paid = models.BooleanField(default=False)
    
    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.product.price)
            if cart_item.size_variant:
                size_variant_price = cart_item.size_variant.price
                price.append(size_variant_price)
                
                
        if self.coupon:
            if self.coupon.minimum_amount < sum(price):
                return sum(price) - self.coupon.discount_price
            
        return sum(price)
                
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null = True, blank=True)
    size_variant = models.ForeignKey(screenSizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    ram_variant = models.ForeignKey(RAMVariant, on_delete=models.SET_NULL, null = True, blank = True)
    product_quantity = models.IntegerField(null = False, blank=False, default=0)
    
    def get_product_price(self):
        price = [self.product.price]
        
        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
        if self.ram_variant:
            ram_variant_price = self.ram_variant.price
            price.append(ram_variant_price)
        return sum(price) 
    
    def get_product_subtotal(self):
        price = [self.product.price]
        
        if self.size_variant:
            size_variant_price = self.size_variant.price
            price.append(size_variant_price)
        if self.ram_variant:
            ram_variant_price = self.ram_variant.price
            price.append(ram_variant_price)
        if self.product.offer:
            self.product.price=self.product.get_offer()
        return sum(price) * self.product_quantity
        
    
