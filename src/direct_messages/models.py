from django.db import models
from accounts.models import MyUser
from django.contrib.auth.signals import user_logged_in

class DirectMessageManager(models.Manager):
    def get_num_unread_messages(self, user):
        return super(DirectMessageManager, self).filter(read=False).filter(receiver=user).count()


class DirectMessage(models.Model):
    subject = models.CharField(max_length=150)
    body = models.CharField(max_length=3000)
    sender = models.ForeignKey(MyUser, related_name='sent_direct_messages', null=True, blank=True)
    receiver = models.ForeignKey(MyUser, related_name='received_direct_messages', null=True, blank=True )
    sent = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    read_at = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)
    read = models.BooleanField(default=False)
    parent = models.ForeignKey('self', related_name='parent_message', null=True, blank=True)
    replied = models.BooleanField(default=False)
    
    
    
    def __unicode__(self):
        return self.subject
    
    objects = DirectMessageManager()
    
    class Meta:
        ordering = ['-sent']
    
def set_messages_in_session(sender, user, request, **kwargs):
    direct_messages = DirectMessage.objects.get_num_unread_messages(user)
    request.session['num_of_messages'] = direct_messages
    
user_logged_in.connect(set_messages_in_session)