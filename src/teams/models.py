from django.db import models
from django.core.urlresolvers import reverse
from accounts.models import MyUser

class Team(models.Model):
    TYPE_CHOICES = (
        ('Intramural','Intramural'),
        ('Club','Club'),
        ('Varsity','Varsity'),
        
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    choice = models.CharField(max_length=30, choices=TYPE_CHOICES )
    description = models.CharField(max_length = 500, null=True, blank=True)
    owner = models.ForeignKey(MyUser, related_name='team_owner', null=True, blank=True)
    team_members = models.ManyToManyField(MyUser, through='TeamMember',related_name='members_of_team')
    slug = models.SlugField( null=True, blank=True)
    logo = models.ImageField(upload_to="teams/", null=True, blank=True)
    
    def __unicode__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("team_page", kwargs={"id":self.id})
    
class TeamMember(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    team_id = models.ForeignKey(Team, null=True, blank=True)
        
    def __unicode__(self, ):
        return str(self.team_id)