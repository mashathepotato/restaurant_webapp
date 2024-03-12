from django.urls import path
from food_advisor import views

app_name = 'food_advisor'

urlpatterns = [
    path('', views.index, name='index'), # No home page url, index is home page.
    # Uncomment when appropriate views are created.
    path('register/', views.registerUser, name='registerUser'),
#     path('register/manager/', views.registerManager, name='register_manager'), # This page also includes restaurant detail entry.
    path('signin/', views.user_signin, name='signin'),
    path('owner/', views.registerOwner, name='owner'),
    path('restaurant/<slug:restaurant_id_slug>/', views.show_restaurant, name='show_restaurant'),
    path('restaurant/<slug:restaurant_id_slug>/reviews/', views.show_restaurant_reviews, name='show_restaurant_reviews'),
    path('restaurant/<slug:restaurant_id_slug>/manage/', views.manage_restaurant, name='manage_restaurant'),
    # path('signout/', views.user_signout, name='signout'),
]