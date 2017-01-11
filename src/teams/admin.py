from django.contrib import admin

from .models import Team, TeamMember

class TeamAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Team
        
admin.site.register(Team, TeamAdmin)


class TeamMemberAdmin(admin.ModelAdmin):
    
    class Meta:
        model = TeamMember
        
        
admin.site.register(TeamMember, TeamMemberAdmin)
