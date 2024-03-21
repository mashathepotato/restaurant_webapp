from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from food_advisor.models import CuisineType, Restaurant, Dish, Review
import os
import restaurant_webapp
from restaurant_webapp import *


class TestHomePage(TestCase):
    def setUp(self):
        self.base_dir = os.getcwd()
        self.template_dir = os.path.join(self.base_dir, 'templates')
        self.about_response = self.client.get(reverse('index'))

    def test_successful_deployment(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_guest_home(self):
        response = self.client.get(reverse("index"))
        self.assertNotEqual(response.status_code, 404)
        self.assertNotContains(response, "Log out")

    def test_user_login_success(self):
        self.client.login(
            username="usertest",
            password="usertest"
        )

        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_manager_login_success(self):
        self.client.login(
            username="username",
            password="userpassword"
        )


class TestRegisterPage(TestCase):
    def setUp(self):
        self.base_dir = os.getcwd()
        self.template_dir = os.path.join(self.base_dir, 'template')
        self.about_response = self.client.get(reverse('food_advisor:registerUser'))

    def test_successful_deployment(self):
        response = self.client.get(reverse("food_advisor:registerUser"))
        self.assertEqual(response.status_code, 200)

    def test_guest_account(self):
        response = self.client.get(reverse("food_advisor:registerUser"))
        self.assertEqual(response.status_code, 200)

    def test_user_login_success(self):
        self.client.login(
            username="usertest",
            password="passwordtest"
        )

        response = self.client.get(reverse("food_advisor:registerUser"))
        self.assertEqual(response.status_code, 200)


class TestLoginPage(TestCase):
    def setUp(self):
        self.base_dir = os.getcwd()
        self.template_dir = os.path.join(self.base_dir, 'templates')
        self.about_response = self.client.get(reverse('food_advisor:signin'))
    
    def test_successful_deployment(self):
        response = self.client.get(reverse("food_advisor:signin"))
        self.assertEqual(response.status_code, 200)

    def test_template_exists(self):
        template_check = os.path.isfile(os.path.join(os.path.join(os.getcwd(), "templates/food_advisor"), "login.html"))
        self.assertTrue(template_check)

    def test_template_account_usage(self):
        self.assertTemplateUsed(self.about_response, "food_advisor/login.html")
   
   
class RegisterManagerViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.cuisine_type1= CuisineType.objects.create(name='Italian')
        self.cuisine_type2= CuisineType.objects.create(name='Japanese')

        self.manager_data = {
            'username': 'test_manager',
            'password1': 'test_password',
            'password2': 'test_password',
            'email': 'test@example.com',
        }

        self.restaurant_data = {
            'name': 'Test Restaurant',
            'address': '123 Test St',
            'timeOpens': '08:00:00',
            'timeCloses': '20:00:00',
            'tags': 'test, restaurant',
            'cuisineTypes': [self.cuisine_type1.pk, self.cuisine_type2.pk],
            'starRating': 4.5,
            'totalReviews': 100,
        }

class ShowRestaurantViewTests(TestCase):
    def setUp(self):
        self.user= User.objects.create_user(username='testuser', password='testpassword')

        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

        self.dish1 = Dish.objects.create(name='Dish 1', restaurant= self.restaurant)
        self.dish2 = Dish.objects.create(name='Dish 2', restaurant= self.restaurant)
    
    # def test_show_restaurant_with_vaild_id(self):
    #     restaurant_id = self.restaurant.id
        
    #     response = self.client.get(reverse('show_restaurant', kwargs={'restaurant_id_slug': restaurant_id}))

    #     self.assertEqual(response.status_code, 200)

    #     self.assertTemplateUsed(response, 'food_advisor/restaurant_detail.html')

    #     self.assertIn('restaurant', response.context)
    #     self.assertIn('dishes', response.context)

    #     self.assertEqual(response.context['restaurant'], self.restaurant)

    #     self.assertIn(self.dish1, response.context['dishes'])
    #     self.assertIn(self.dish2, response.context['dishes'])

    # def test_show_restaurant_with_invalid_id(self):
    #     invalid_restaurant_id = 9999

    #     response = self.client.get(reverse('show_restaurant', kwargs={'restaurant_id_slug': invalid_restaurant_id}))

    #     self.assertEqual(response.status_code, 200)

    #     self.assertTemplateUsed(response, 'food_advisor/restaurant_detail.html')

    #     self.assertNotIn('restaurant', response.context)
    #     self.assertNotIn('dishes', response.context)



class ShowRestaurantReviewsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.review1= Review.objects.create(restaurant=self.restaurant, content='Great food!', starRating=5)
        self.review2= Review.objects.create(restaurant=self.restaurant, content='Poor service!', starRating=2)

    
    # def test_show_restaurant_reviews_with_valid_id(self):
    #     response = self.client.get(reverse('show_restaurant_reviews', kwargs={'restaurant_id_slug': self.restaurant.id}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'food_advisor/show_restaurant_reviews.html')
    #     self.assertIn('restaurant', response.context)
    #     self.assertIn('reviews', response.context)
    #     self.assertEqual(response.context['restaurant'], self.restaurant)
    #     self.assertIn(self.review1, response.context['reviews'])
    #     self.assertIn(self.review2, response.context['reviews'])


    # def test_show_restaurant_reviews_with_invalid_id(self):
    #     invalid_restaurant_id = 9999
    #     response = self.client.get(reverse('show_restaurant_reviews', kwargs={'restaurant_id_slug': invalid_restaurant_id}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'food_advisor/show_restaurant_reviews.html')
    #     self.assertNotIn('restaurant', response.context)
    #     self.assertNotIn('reviews', response.context)
