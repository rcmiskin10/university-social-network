from django.contrib import admin

from .models import DirectMessage

class DirectMessageAdmin(admin.ModelAdmin):
    
    class Meta:
        model = DirectMessage
        
admin.site.register(DirectMessage, DirectMessageAdmin)