from django.db import models
from django.core.urlresolvers import reverse
from accounts.models import MyUser


class Frat(models.Model):
    FRAT_OR_SORORITY_CHOICES = (
        ('Fraternity','Fraternity'),
        ('Sorority','Sorority'),
        
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    frat_or_sorority = models.CharField(max_length=15, choices=FRAT_OR_SORORITY_CHOICES )
    description = models.CharField(max_length = 500, null=True, blank=True)
    owner = models.ForeignKey(MyUser, related_name='frat_owner', null=True, blank=True)
    members = models.ManyToManyField(MyUser, through='Member',related_name='members_of_frat')
    slug = models.SlugField( null=True, blank=True)
    logo = models.ImageField(upload_to="frats/", null=True, blank=True)
    
    def __unicode__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse("frat_page", kwargs={"id":self.id})
    
class Member(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    frat_id = models.ForeignKey(Frat, null=True, blank=True)
        
    def __unicode__(self, ):
        return str(self.frat_id)