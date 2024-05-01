# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class VolantUser(AbstractUser):
    email = models.EmailField(max_length=100,unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)
    nic = models.CharField(max_length=15, unique=True)
    interests = models.TextField(max_length=100,blank=True)
    abilities = models.TextField(max_length=100,blank=True)
    talents = models.TextField(max_length=100,blank=True)

    # Add unique related_name for groups and user_permissions fields
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='volantuser_set',  # or any other unique name you prefer
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='volantuser_set',  # or any other unique name you prefer
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
