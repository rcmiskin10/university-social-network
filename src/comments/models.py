from django.db import models

from accounts.models import MyUser
from course.models import Course
from clubs.models import Club
from teams.models import Team
from frats.models import Frat
from local.models import Place

class MyPostManager(models.Manager):
    
    def create_mypost(self, user=None, place=None, club=None, profile=None, frat=None, team=None, course=None, main= None, text=None, path=None, links = None, image = None, parent=None):
        
        if not user:
            ValueError("Must include a path when adding Comment")
            
        mypost= self.model(
            user = user,
            path = path,
            text = text,
            links = links,
            image = image,
            main = main,
            course = course,
            club = club,
            team = team,
            frat = frat,
            profile = profile,
            place=place
            
        )
        if parent is not None:
            mypost.parent = parent
        
        mypost.save(using=self._db)
        return mypost

class MyPost(models.Model):
    EVENT_CHOICES = (
        ('Party', 'Party'),
        ('Game', 'Game'),
        ('General Event', 'General Event'),
        
    )
    HOUR_CHOICES = (
        ('12AM','12AM'),
        ('1AM','1AM'),
        ('2AM','2AM'),
        ('3AM','3AM'),
        ('4AM','4AM'),
        ('5AM','5AM'),
        ('6AM','6AM'),
        ('7AM','7AM'),
        ('8AM','8AM'),
        ('9AM','9AM'),
        ('10AM','10AM'),
        ('11AM','11AM'),
        ('12PM','12PM'),
        ('1PM','1PM'),
        ('2PM','2PM'),
        ('3PM','3PM'),
        ('4PM','4PM'),
        ('5PM','5PM'),
        ('6PM','6PM'),
        ('7PM','7PM'),
        ('8PM','8PM'),
        ('9PM','9PM'),
        ('10PM','10PM'),
        ('11PM','11PM'),
        
    )
    user = models.ForeignKey(MyUser)
    parent = models.ForeignKey('self', null=True, blank=True)
    path = models.CharField(max_length=350, null=True, blank=True)
    course = models.ForeignKey(Course, null=True, blank=True)
    profile = models.ForeignKey(MyUser, null=True, blank=True, related_name='profile_user')
    club = models.ForeignKey(Club, null=True, blank=True)
    frat = models.ForeignKey(Frat, null=True, blank=True)
    team = models.ForeignKey(Team, null=True, blank=True)
    place = models.ForeignKey(Place, null=True, blank=True)
    main = models.CharField(max_length=20, null=True, blank=True )
    text = models.TextField()
    links = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to='image_posts/', null=True, blank=True)
    event = models.CharField(max_length=20, choices=EVENT_CHOICES, default=None, null=True, blank=True)
    start_time = models.CharField(max_length=10, choices=HOUR_CHOICES, null=True, blank=True)
    end_time = models.CharField(max_length=10, choices=HOUR_CHOICES, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    likes = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    objects = MyPostManager()
    
    class Meta:
        ordering = ['-timestamp']
    def __unicode__(self):
        return str(self.text)
    
    @property
    def get_mypost(self):
        return self.text
    
    @property
    def is_child(self):
        if self.parent is not None:
            return True
        else:
            return False
    
    def get_children(self):
        if self.is_child:
            return None
        else:
            return MyPost.objects.filter(parent=self)
    
