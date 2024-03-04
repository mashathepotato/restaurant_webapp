from django.db import models


class User(models.Model):
    userId = models.IntegerField(default=0, primary_key=True)
    regDate = models.IntegerField()
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField()
    
    def __str__(self):
        return self.username


class Restaurant(models.Model):
    restaurantId = models.IntegerField(default=0, primary_key=True)
    address = models.CharField(max_length=128)
    timeOpens = models.TimeField()
    timeCloses = models.TimeField()
    url = models.URLField()
    tags = models.CharField(max_length=128)
    cuisineType = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name

class Review(models.Model):
    reviewId = models.IntegerField(default=0)
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(1280)
    date = models.DateTimeField(auto_now_add=True)
    replyContent = models.CharField(128)
    
    def __str__(self):
        return self.reviewId

class Dish(models.Model):
    dishId = models.IntegerField(default=0)
    restaurantId = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    price = models.IntegerField(max_length=64)

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return self.name
    
#tags in Restaurant might be more spphisticated
#changed the restaurant times to time opens and time closes
#changed the length of review content field to 1280 from the er diagram