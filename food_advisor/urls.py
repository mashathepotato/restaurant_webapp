from django.urls import path
from food_advisor import views

app_name = 'food_advisor'

urlpatterns = [
    path('', views.index, name='index'), # No home page url, index is home page.

    # Uncomment when appropriate views are created.
    path('register/', views.registerUser, name='registerUser'),
    # path('register/manager/', views.registerManager, name='registerManager'), # This page also includes restaurant detail entry.
    path('signin/', views.user_signin, name='signin'),
    path('owner/', views.registerOwner, name='owner'),
    # path('restaurant/<slug:restaurant_id_slug>/', views.show_restaurant, name='showRestaurant'),
    # path('restaurant/<slug:restaurant_id_slug>/manage/', views.manage_restaurant, name="manageRestaurant"),
    # path('signout/', views.user_signout, name='signout'),
]