from django.contrib import admin
from food_advisor.models import User, Restaurant, Review, Dish

admin.site.register(Restaurant)
admin.site.register(Review)
admin.site.register(Dish)
