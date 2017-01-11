from django.db import models

from accounts.models import MyUser

class ProfileInfo(models.Model):
    YEAR_CHOICES = (
        ('Class of 2016', 'Class of 2016'),
        ('Class of 2017', 'Class of 2017'),
        ('Class of 2018', 'Class of 2018'),
        ('Class of 2019', 'Class of 2019'),
        ('Alumni', 'Alumni'),
        
    )
    user = models.ForeignKey(MyUser, null=True, blank=True)
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    minor = models.CharField(max_length=100, null=True, blank=True)
    loc_from = models.CharField(max_length=100, null=True, blank=True)
    
    def __unicode__(self, ):
        return self.user.email
   
class UserPicture(models.Model):
    user = models.ForeignKey(MyUser)
    image = models.ImageField(upload_to='profiles/')
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    def __unicode__(self, ):
        return str(self.image)
    
    
        

class Post(models.Model):
    author = models.ForeignKey(MyUser)
    text = models.TextField()

    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

    def __unicode__(self):
        return self.text+' - '+self.author.username

class Bio(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    bio = models.TextField()

    def __unicode__(self, ):
        return self.user.username

class Work(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200)

    def __unicode__(self, ):
        return self.user.username

class Interest(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    interest = models.CharField(max_length=100)
    
    def __unicode__(self, ):
        return self.user.username

class DreamJob(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    dream_job = models.CharField(max_length=100)
    
    def __unicode__(self, ):
        return self.user.username