from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from food_advisor.models import CuisineType, Restaurant, Dish, Review


class RegisterUserViewTests(TestCase):
    def test_successful_registration(self):
        post_data= {
            'username': 'test_user',
            'email': 'test@example.com',
            'passowrd1': 'test_password',
            'password2': 'test_password',
            'isManager': False,
        }
        response = self.client.post(reverse('register_user'), post_data)

        self.assertRedirects(response, reverse('food_advidor:index'))
        self.assertTrue(User.objects.filter(username='test_user').exists())


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

    def test_register_manager(self):
        response = self.client.post(reverse('register_manager'), {
            **self.manager_data,
            **self.restaurant_data
        })

        self.assertRedirects(response, reverse('food_advisor:index'))

        self.assertTrue(User.objects.filter(username='test_manager').exists())
        self.assertTrue(User.objects.get(username='test_manager').is_manager)
        self.assertTrue(User.objects.get(username='test_manager').restaurant_set.exists())


class UserLoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user= User.objects.create_user(username='testuser', password='testpassword')

    def test_user_login_success(self):
        response = self.client.post(reverse('user_login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertRedirects(response, reverse('food_advisor:index'))
        self.assertTrue('_auth_user_id' in self.client.session)
    
    def test_user_login_inactive(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(reverse('user_login', {'username': 'testuser', 'password': 'testpassword'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your FoodAdvisor account is disabled.')
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_user_login_invalid_details(self):
        response = self.client.post(reverse('user_login', {'username': 'testuser', 'password': 'testpassword'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid login details.')
        self.assertFalse('_auth_user_id' in self.client.session)

class ShowRestaurantViewTests(TestCase):
    def setUp(self):
        self.user= User.objects.create_user(username='testuser', password='testpassword')

        self.restaurant = Restaurant.objects.create(name='Test Restaurant')

        self.dish1 = Dish.objects.create(name='Dish 1', restaurant= self.restaurant)
        self.dish2 = Dish.objects.create(name='Dish 2', restaurant= self.restaurant)
    
    def test_show_restaurant_with_vaild_id(self):
        restaurant_id = self.restaurant.id
        
        response = self.client.get(reverse('show_restaurant', kwargs={'restaurant_id_slug': restaurant_id}))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'food_advisor/restaurant_detail.html')

        self.assertIn('restaurant', response.context)
        self.assertIn('dishes', response.context)

        self.assertEqual(response.context['restaurant'], self.restaurant)

        self.assertIn(self.dish1, response.context['dishes'])
        self.assertIn(self.dish2, response.context['dishes'])

    def test_show_restaurant_with_invalid_id(self):
        invalid_restaurant_id = 9999

        response = self.client.get(reverse('show_restaurant', kwargs={'restaurant_id_slug': invalid_restaurant_id}))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'food_advisor/restaurant_detail.html')

        self.assertNotIn('restaurant', response.context)
        self.assertNotIn('dishes', response.context)



class ShowRestaurantReviewsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.restaurant = Restaurant.objects.create(name='Test Restaurant')
        self.review1= Review.objects.create(restaurant=self.restaurant, content='Great food!', starRating=5)
        self.review2= Review.objects.create(restaurant=self.restaurant, content='Poor service!', starRating=2)

    
    def test_show_restaurant_reviews_with_valid_id(self):
        response = self.client.get(reverse('show_restaurant_reviews', kwargs={'restaurant_id_slug': self.restaurant.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_advisor/show_restaurant_reviews.html')
        self.assertIn('restaurant', response.context)
        self.assertIn('reviews', response.context)
        self.assertEqual(response.context['restaurant'], self.restaurant)
        self.assertIn(self.review1, response.context['reviews'])
        self.assertIn(self.review2, response.context['reviews'])


    def test_show_restaurant_reviews_with_invalid_id(self):
        invalid_restaurant_id = 9999
        response = self.client.get(reverse('show_restaurant_reviews', kwargs={'restaurant_id_slug': invalid_restaurant_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'food_advisor/show_restaurant_reviews.html')
        self.assertNotIn('restaurant', response.context)
        self.assertNotIn('reviews', response.context)


