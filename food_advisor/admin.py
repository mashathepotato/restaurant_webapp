from django.contrib import admin
from food_advisor.models import CuisineType, Restaurant, Review, Dish, UserProfile

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Dish)
admin.site.register(UserProfile)
admin.site.register(CuisineType)