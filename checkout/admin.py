from django.contrib import admin
from . models import Order, Payment_methods, Order_item

# Register your models here.
class OrderItemTableInline(admin.TabularInline):
    model=Order_item
    
class OrderAdmin(admin.ModelAdmin):
    inlines= [OrderItemTableInline]
    
admin.site.register(Order,OrderAdmin)

admin.site.register(Payment_methods)