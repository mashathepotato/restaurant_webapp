from django.urls import path
from food_advisor import views

app_name = 'food_advisor'

urlpatterns = [
    path('', views.index, name='index'), # No home page url, index is home page.
    # path('register/', views.registerUser, name='register_user'),
    # path('register/manager/', views.registerManager, name='register_manager'), # This page also includes restaurant detail entry.
    # path('signin/', views.user_signin, name='signin'),
    path('restaurant/<slug:restaurant_id_slug>/', views.show_restaurant, name='show_restaurant'),
    path('restaurant/<slug:restaurant_id_slug>/reviews/', views.show_restaurant_reviews, name='show_restaurant_reviews'),
    path('restaurant/<slug:restaurant_id_slug>/manage/', views.manage_restaurant, name='manage_restaurant'),
    # path('signout/', views.user_signout, name='signout'),
]