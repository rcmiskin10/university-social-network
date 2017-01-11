from django.contrib import admin

from .models import TeamSchedule

class TeamScheduleAdmin(admin.ModelAdmin):
    
    class Meta:
        model = TeamSchedule
        
admin.site.register(TeamSchedule, TeamScheduleAdmin)
