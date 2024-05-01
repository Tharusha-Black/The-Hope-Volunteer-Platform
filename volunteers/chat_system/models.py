from django.db import models
from django.conf import settings
from volunteer_oppertunities.models import VolantProjects

class PrivateChat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='private_chats')

class GroupChat(models.Model):
    project = models.ForeignKey(VolantProjects, on_delete=models.CASCADE, related_name='group_chats')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_chats')

class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(PrivateChat, on_delete=models.CASCADE, null=True, blank=True)
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE, null=True, blank=True)
