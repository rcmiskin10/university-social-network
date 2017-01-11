from django.contrib import admin

from .models import Club, ClubMember

class ClubAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Club
        
admin.site.register(Club, ClubAdmin)


class ClubMemberAdmin(admin.ModelAdmin):
    
    class Meta:
        model = ClubMember
        
        
admin.site.register(ClubMember, ClubMemberAdmin)