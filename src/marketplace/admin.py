from django.contrib import admin

from .models import Product, Category

class CategoryAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Category
        
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Product
        
admin.site.register(Product, ProductAdmin)