from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from accounts.models import MyUser
from django.core.files.storage import FileSystemStorage





def download_loc(instance, filename):
    return "%s_%s" %(instance.user.username, filename)
class Course(models.Model):
    course_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    course_code = models.IntegerField( null=True, blank=True)
    course_num = models.CharField(max_length=50, null=True, blank=True)
    course_time = models.CharField(max_length=50,null=True, blank=True)
    course_professor = models.CharField(max_length=100, null=True, blank=True)
    students = models.ManyToManyField(MyUser, through='StudentCourse')
    slug = models.SlugField(unique=True, null=True, blank=True)

    
    
    
    def __unicode__(self, ):
        return str(self.course_name)

    def get_absolute_url(self):
        return reverse("course_page", kwargs={"slug":self.slug})
    
class StudentCourse(models.Model):
    user = models.ForeignKey(MyUser, null=True, blank=True)
    course_id = models.ForeignKey(Course, null=True, blank=True)
        
    def __unicode__(self, ):
        return self.user.email


class Syllabus(models.Model):
    user = models.ForeignKey(MyUser)
    path = models.CharField(max_length=350)
    course = models.ForeignKey(Course, null=True, blank=True)
    syllabus = models.FileField(upload_to=download_loc)
    html = models.TextField(null=True, blank=True)
    def __unicode__(self, ):
        return str(self.user)
    

class Assignment(models.Model):
    user = models.ForeignKey(MyUser)
    course = models.ForeignKey(Course, null=True, blank=True)
    name = models.CharField(max_length=300)
    due_date = models.CharField(max_length=300)

    def __unicode__(self, ):
        return str(self.user)

class CourseNote(models.Model):
    user = models.ForeignKey(MyUser)
    path = models.CharField(max_length=350)
    course = models.ForeignKey(Course, null=True, blank=True)
    text = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self, ):
        return self.user.email

