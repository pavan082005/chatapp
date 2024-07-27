from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    friends = models.ManyToManyField('Friend', "my_friends")

    def __str__(self):
        return self.name

class Friend(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.name

class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipient')
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.content