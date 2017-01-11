from django.contrib import admin

from .models import ProfileInfo, Work, Interest, Bio, UserPicture

class ProfileInfoAdmin(admin.ModelAdmin):
    
    class Meta:
        model = ProfileInfo
        
admin.site.register(ProfileInfo, ProfileInfoAdmin)

class WorkAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Work
        
admin.site.register(Work, WorkAdmin)

class InterestAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Interest
        
admin.site.register(Interest, InterestAdmin)

class BioAdmin(admin.ModelAdmin):
    
    class Meta:
        model = Bio
        
admin.site.register(Bio, BioAdmin)

class UserPictureAdmin(admin.ModelAdmin):
    
    class Meta:
        model = UserPicture
        
admin.site.register(UserPicture, UserPictureAdmin)