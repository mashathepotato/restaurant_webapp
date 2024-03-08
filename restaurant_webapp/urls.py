from django.contrib import admin
from django.urls import path
from django.urls import include
from food_advisor import views

urlpatterns = [
    path('', views.index, name='index'),
    path('food_advisor/', include('food_advisor.urls')),
    path('admin/', admin.site.urls),
    path('nothing/', views.nothing, name='nothing'),
]
