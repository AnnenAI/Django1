from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Dialogue(models.Model):
    users = models.ManyToManyField(User,related_name='dialogue')
    last_message_date = models.DateTimeField(default=timezone.localtime(timezone.now()))

    class Meta:
        ordering = ["-last_message_date"]

    def __str__(self):
        return str(self.last_message_date)+' | '+str(self.users)

class Message(models.Model):
    date_sending = models.DateTimeField(default=timezone.localtime(timezone.now()))
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    dialogue = models.ForeignKey(Dialogue,related_name='messages', on_delete=models.CASCADE)

    class Meta:
         ordering = ["-date_sending"]

    def __str__(self):
        return '%s %s - %s' %(self.author.first_name,self.author.second_name,self.date_sending)
