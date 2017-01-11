from django.db import models
from accounts.models import MyUser


class Product(models.Model):
	

	owner = models.ForeignKey(MyUser, null=True, blank=True)
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=200)
	category = models.ForeignKey('Category', related_name='cat')
	price = models.CharField(max_length=100)
	order = models.IntegerField(default=0)
	sold = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	image = models.ImageField(upload_to="products/", null=True, blank=True)

	def __unicode__(self):
	    return str(self.title)

	class Meta:
	    ordering = ['-order']
    
class Category(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
	    return str(self.name)