from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Dialogue(models.Model):
    last_message_date = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ["-last_message_date"]

    def __str__(self):
        return str(self.last_message_date)

class Users(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name='members' ,on_delete=models.CASCADE)
    dialogue = models.ForeignKey(Dialogue, related_name='users', on_delete=models.CASCADE)


class Message(models.Model):
    date_sending = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()
    dialogue = models.ForeignKey(Dialogue,related_name='messages', on_delete=models.CASCADE)

    class Meta:
         ordering = ["date_sending"]

    def __str__(self):
        return '%s %s - %s' %(self.author.first_name,self.author.last_name,self.date_sending)
