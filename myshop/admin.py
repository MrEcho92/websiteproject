from django.contrib import admin
from .models import Category,Product, Order, OrderProduct
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'stock', 'available', 'created_on', 'updated_on']
    list_filter = ['available', 'created_on', 'updated_on', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Product, ProductAdmin)

admin.site.register(Order)
admin.site.register(OrderProduct)
