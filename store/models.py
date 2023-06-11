from django.db import models
from django.utils.text import slugify
import random
from category.models import Category

# Create your models here.
# BRAND MODEL
class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique = True)
    brand_image = models.ImageField(upload_to='photos/brand', default = 'No image available')
    brand_address = models.TextField(max_length=200)
    brand_description = models.TextField(max_length=300) 
    
    
    def save(self, *args, **kwargs):
        # generate slug field from name field if slug is empty
        if not self.slug:
            self.slug = slugify(self.brand_name)
        super(Brand, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.brand_name
    
class screenSizeVariant(models.Model):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.size_name
    
class RAMVariant(models.Model):
    RAM_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.RAM_name
    
class price_filter(models.Model):
    filter_price = (
        
        ('1000 TO 10000', '1000 TO 10000'),
        ('10000 TO 20000', '10000 TO 20000'),
        ('20000 TO 30000', '20000 TO 30000'),
        ('30000 TO 40000', '30000 TO 40000'),
        ('40000 TO 50000', '40000 TO 50000'),
        ('50000 and above', '50000 and above'),
        
        )
    price = models.CharField(choices=filter_price, max_length=60)
    
    def __str__(self):
        return self.price
    
    
class Offer(models.Model):
    offer_name = models.CharField(max_length=100)
    discount_amount = models.PositiveIntegerField()
    
    def __str__(self):
        return self.offer_name


def generate_product_id():
    """Generate a unique four-digit product ID."""
    while True:
        new_id = random.randint(1000, 9999)
        if not Product.objects.filter(identification=new_id).exists():
            return new_id


class Product(models.Model):
    identification = models.IntegerField(default=generate_product_id,null=True)
    product_name = models.CharField(unique=True,max_length=50)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    product_description = models.TextField(blank=True)
    screensize_variant = models.ManyToManyField(screenSizeVariant, blank=True)
    ram_variant = models.ManyToManyField(RAMVariant, blank=True)
    price = models.PositiveIntegerField(default=0)
    filt_price = models.ForeignKey(price_filter, on_delete=models.CASCADE, null=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True, blank=True )
    

    def __str__(self):
        return self.product_name
    
    def get_product_price_by_size(self, size):
        return self.price + screenSizeVariant.objects.get(size_name = size).price
    
    def get_offer(self):
        return self.price - self.offer.discount_amount
    

class Product_Image(models.Model):
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/product')
   
    def __str__(self) -> str:
        return str(self.product)

    

