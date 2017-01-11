from django.contrib import admin

from .models import Frat, Member

class FratAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Frat
        
admin.site.register(Frat, FratAdmin)

from django.contrib import admin

from .models import Frat

class MemberAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Member
        
admin.site.register(Member, MemberAdmin)