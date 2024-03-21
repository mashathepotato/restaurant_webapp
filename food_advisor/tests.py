from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from food_advisor.models import CuisineType, Restaurant, Dish, Review
import os


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
   