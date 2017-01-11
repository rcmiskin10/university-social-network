from django.contrib import admin

from .models import FratSchedule

class FratScheduleAdmin(admin.ModelAdmin):
    
    class Meta:
        model = FratSchedule
        
admin.site.register(FratSchedule, FratScheduleAdmin)