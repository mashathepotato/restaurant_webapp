from django.urls import path
from food_advisor import views


app_name = 'food_advisor'

urlpatterns = [
    path('', views.index, name='index'), # No home page url, index is home page.
    # Uncomment when appropriate views are created.
    path('register/', views.register_user, name='registerUser'),
    path('signin/', views.user_login, name='signin'),
    path('owner/', views.register_manager, name='owner'),
    path('restaurant/<slug:restaurant_id_slug>/', views.show_restaurant, name='show_restaurant'),
    path('restaurant/<slug:restaurant_id_slug>/reviews/', views.show_restaurant_reviews, name='show_restaurant_reviews'),
    path('restaurant/<slug:restaurant_id_slug>/reviews/<slug:review_id>', views.review_reply, name='review_reply'),
    path('restaurant/<slug:restaurant_id_slug>/manage/', views.manage_restaurant, name='manage_restaurant'),
    path('signout/', views.user_logout, name='signout'),
    path('ajax/add_dish/<slug:restaurant_id_slug>/', views.add_dish_ajax, name='add_dish_ajax'),
    path('ajax/delete_dish/<int:dish_id>/', views.delete_dish_ajax, name='delete_dish_ajax'),
]