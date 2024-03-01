from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from taggit.managers import TaggableManager


class FoodType(models.Model):
    title = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(default=timezone.now)

class FoodPost(models.Model):
    column = models.ForeignKey(
        FoodType,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='food'
    )
    tags = TaggableManager(blank=True)
    avatar = models.ImageField(upload_to='food/%Y%m%d/', blank=True)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)