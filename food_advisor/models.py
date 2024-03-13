from django.db import models
from django.contrib.auth.models import User
import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    isManager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

STAR_CHOICES = [
        (0, '0 stars'),
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ]

class CuisineType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name



class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    manager = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    address = models.CharField(max_length=128)
    timeOpens = models.TimeField(default='12:00:00')
    timeCloses = models.TimeField(default='12:00:00')
    tags = models.CharField(max_length=128, blank=True, default="")
    cuisineTypes = models.ManyToManyField(CuisineType, blank=True)
    name = models.CharField(max_length=128)
    starRating = models.DecimalField(decimal_places=4, max_digits=10, default=0)
    totalReviews = models.IntegerField(default=0)
    image = models.ImageField(upload_to='restaurant_images', blank=True)
    
    def __str__(self):
        return self.name
    
    def getIntegerStars(self):
        # Rounds average stars to integer for displaying star images.
        return int(round(self.starRating))
    
    def getTags(self):
        return self.tags.split(",")
    
    def getCuisines(self):
        list = []
        for type in self.cuisineTypes.all():
            list.append(str(type.name))
        return list

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1280)
    date = models.DateTimeField(auto_now_add=True)
    replyContent = models.CharField(max_length=128, default='')
    starRating = models.IntegerField(choices = STAR_CHOICES, default=0)
    def __str__(self):
        return str(self.id)

class Dish(models.Model):
    id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    price = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return self.name
    
#tags in Restaurant might be more spphisticated
#changed the restaurant times to time opens and time closes
#changed the length of review content field to 1280 from the er diagram
