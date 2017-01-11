from django.contrib import admin

from .models import Place, PlaceCategory

class PlaceCategoryAdmin(admin.ModelAdmin):
    
    class Meta:
        model = PlaceCategory
        
admin.site.register(PlaceCategory, PlaceCategoryAdmin)

class PlaceAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Place
        
admin.site.register(Place, PlaceAdmin)