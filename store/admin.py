from django.contrib import admin
from . models import Brand,Product,Product_Image, screenSizeVariant, RAMVariant,price_filter, Offer

# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('brand_name',)}
    
admin.site.register(Brand, BrandAdmin)

class Product_ImageAdmin(admin.StackedInline):
    model = Product_Image
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [Product_ImageAdmin]
    
admin.site.register(Product_Image)
admin.site.register(Product, ProductAdmin)

@admin.register(screenSizeVariant)
class screenSizeVariantAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'price', 'stock']
    model = screenSizeVariant
    
  
@admin.register(RAMVariant)    
class RAMVariantAdmin(admin.ModelAdmin):
    list_display = ['RAM_name', 'price', 'stock']
    model = RAMVariant
    
    
admin.site.register(price_filter)

admin.site.register(Offer)