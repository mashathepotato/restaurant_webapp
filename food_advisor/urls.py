from django.urls import path
from food_advisor import views

app_name = 'food_advisor'

urlpatterns = [
    path('', views.index, name='index'), # No home page url, index is home page.
    # Uncomment when appropriate views are created.
    path('register/', views.register_user, name='registerUser'),
    path('login/', views.user_login, name='user_login'),
    path('owner/', views.register_manager, name='owner'),
    path('restaurant/<slug:restaurant_id_slug>/', views.show_restaurant, name='show_restaurant'),
    path('restaurant/<slug:restaurant_id_slug>/reviews/', views.show_restaurant_reviews, name='show_restaurant_reviews'),
    path('restaurant/<slug:restaurant_id_slug>/manage/', views.manage_restaurant, name='manage_restaurant'),
    path('signout/', views.user_logout, name='signout'),
]