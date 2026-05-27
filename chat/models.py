from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('mod', 'Moderator'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    is_blocked = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=True, null=True)

class Channel(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, blank=True, related_name='channels')

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Reaction(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('message', 'user', 'emoji')


class DirectMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_direct_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_direct_messages')
    content = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
