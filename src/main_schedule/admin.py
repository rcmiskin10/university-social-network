from django.contrib import admin
from .models import MainSchedule


class MainScheduleAdmin(admin.ModelAdmin):
    
    class Meta:
        model = MainSchedule
        
admin.site.register(MainSchedule, MainScheduleAdmin)
