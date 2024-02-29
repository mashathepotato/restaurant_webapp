from django.urls import path
from food_advisor import views

app_name = 'food_advisor'

urlpatterns = [
    path('', views.index, name='index'),
]