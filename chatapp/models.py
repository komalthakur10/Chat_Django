from django.db import models

from django.contrib.auth.models import User # By default django has a table for User (in mysql as "auth_user")
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your models here.

# Message table/model

class Msg(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name="send_msg", db_index = True) 
    receiver = models.ForeignKey(User, on_delete = models.CASCADE, related_name="recv_msg", db_index = True)
    content = models.TextField('content')
    timestamp = models.DateTimeField(auto_now_add = True)    

    # ForeignKey - user is referred from User table.
    # CASCADE - When sender user is deleted also delete its related data.

    def __str__(self):
        return f"{self.id}"

    def notify_ws_clients(self):
        notification = {
            'type': 'receive_group_message',
            'message': f"{self.id}"
        }
        channel_layer = get_channel_layer()
#        print("user.sender.id = ",self.sender.id)
#        print("user.receiver.id = ",self.receiver.id)
        async_to_sync(channel_layer.group_send)(f"{self.sender.id}", notification)
        async_to_sync(channel_layer.group_send)(f"{self.receiver.id}", notification)

    def save(self, *args, **kwargs):
#        print("save started")
        new = self.id
        self.content = self.content.strip()
        super(Msg, self).save(*args, **kwargs)
#        print("New :", new)
        if new is None:
            self.notify_ws_clients()

    class Meta:
        app_label = 'chatapp'
        ordering = ('-timestamp',)

 
# Profile table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='Profile/default.png', upload_to ='Profile')

    def __str__(self):
        return f"{ self.user.username } Profile"