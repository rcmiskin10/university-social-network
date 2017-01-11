from django.db import models


class Place(models.Model):
	image = models.ImageField(upload_to="local/", null=True, blank=True)
	name = models.CharField(max_length=100)
	category = models.ManyToManyField('PlaceCategory', related_name='cat')
	rating = models.CharField(max_length=20)
	address = models.CharField(max_length=200)
	website = models.URLField(max_length=300, null=True, blank=True)
	delivery = models.BooleanField(default=False)
	hours = models.CharField(max_length=100, null=True, blank=True)
	latitude = models.CharField(max_length=50)
	longitude = models.CharField(max_length=50)
	menu = models.URLField(max_length=300, null=True, blank=True)
	phone = models.CharField(max_length=20)
	distance = models.CharField(max_length=50)

	def __unicode__(self):
	    return str(self.name)

    
class PlaceCategory(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
	    return str(self.name)


