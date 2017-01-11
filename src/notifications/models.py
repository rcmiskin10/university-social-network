from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from accounts.models import MyUser
from .signals import notify
from clubs.models import Club


class Notification(models.Model):
	sender = models.ForeignKey(MyUser, related_name='sender_user', null=True, blank=True)
	recipient = models.ForeignKey(MyUser, related_name='reciepient_user', null=True, blank=True)
	action = models.CharField(max_length=255, null=True, blank=True)
	
	target_content_type = models.ForeignKey(ContentType, null=True, blank=True)
	target_object_id = models.PositiveIntegerField(null=True, blank=True)
	target_object = GenericForeignKey("target_content_type", "target_object_id")
	read = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	class Meta:
		ordering = ['-timestamp']
	def __unicode__(self):
		return self.action


def new_notification(sender, **kwargs):
	kwargs.pop('signal', None)
	recipient = kwargs.pop("recipient")
	
	action = kwargs.pop("action")
	target = kwargs.pop("target", None)
	affected_users = kwargs.pop('affected_users', None)
	print affected_users
	if affected_users is not None:
		for u in affected_users:
			print u
			new_note = Notification(

				recipient = u,
				action = action,
				sender = sender,
				)
			

			if target is not None:
				new_note.target_content_type = ContentType.objects.get_for_model(target)
				new_note.target_object_id = target.id
				
			new_note.save()

	if target is None:

		new_note = Notification(

				recipient = recipient,
				action = action,
				sender = sender,
				)

		new_note.save()

notify.connect(new_notification)