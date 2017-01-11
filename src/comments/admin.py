from django.contrib import admin

from .models import MyPost

class MyPostAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','text','timestamp' ]
    class Meta:
        model = MyPost
        
admin.site.register(MyPost, MyPostAdmin)