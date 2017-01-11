from django.db import models
from django.core.urlresolvers import reverse
from accounts.models import MyUser

class Club(models.Model):
    club_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length = 500, null=True, blank=True)
    owner = models.ForeignKey(MyUser, related_name='group_owner', null=True, blank=True)
    club_members = models.ManyToManyField(MyUser, through='ClubMember',related_name='members_of_club')
    slug = models.SlugField( null=True, blank=True)
    logo = models.ImageField(upload_to="clubs/", null=True, blank=True)
    
    def __unicode__(self):
        return str(self.club_name)
    def get_absolute_url(self):
        return reverse("club_page", kwargs={"id":self.id})
    
class ClubMember(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    club_id = models.ForeignKey(Club, null=True, blank=True)
        
    def __unicode__(self, ):
        return str(self.club_id)
