from django.contrib import admin

from .models import Schedule

class ScheduleAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Schedule
        
admin.site.register(Schedule, ScheduleAdmin)
