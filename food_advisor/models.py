from django.db import models
from django.contrib.auth.models import User

# This is an altered version of Madison's models, takes into account
# that Django already provides a User model, removes unnecessary IDs,
# and implements a few additional fields.

# Using django's user auth model, already takes care of username,
# email, password etc...

class Restaurant(models.Model):
    address = models.CharField(max_length=128)
    timeOpens = models.TimeField(null=True)
    timeCloses = models.TimeField()
    url = models.URLField()
    tags = models.CharField(max_length=128) # Tags are comma separated strings.
    cuisineType = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    avg_stars = models.DecimalField(decimal_places=4, max_digits=10)
    total_ratings = models.IntegerField()

    # Establish one to one relationship between managers and restaurants,
    # doing it here means users are only managers when linked to a restaurant.
    manager = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        # Note CASCADE, restaurants cannot exist without a manager.
        primary_key=False,
    )

    class Meta:
        verbose_name_plural = 'Restaurants'
    
    def __str__(self):
        return self.name

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=1280)
    date = models.DateTimeField(auto_now_add=True)
    replyContent = models.CharField(max_length=1280)
    starRating = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Reviews'
    
    def __str__(self):
        return (self.user.username + self.restaurant.name)

class Dish(models.Model):
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
