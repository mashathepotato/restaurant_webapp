from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Dish, UserProfile


from food_advisor.models import CuisineType, Restaurant, Review, STAR_CHOICES

from food_advisor.models import CuisineType, Restaurant

User = get_user_model()



# UserForm for user registration
class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Add a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# ManagerRegistrationForm for manager registration
class ManagerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Add a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.isManager = True  # Ensure your User model supports this attribute
        if commit:
            user.save()
        return user

class RestaurantEditForm(forms.ModelForm):
    name = forms.CharField(max_length=128, label="Name")
    address = forms.CharField(max_length=128, label="Address")
    timeOpens = forms.TimeField(label="Opening Time")
    timeCloses = forms.TimeField(label="Closing Time")
    tags = forms.CharField(max_length=128, label="Tags")
    cuisineTypes = forms.ModelMultipleChoiceField(queryset=CuisineType.objects.all(),
                                                  label="Cuisine Type",
                                                  widget=forms.CheckboxSelectMultiple,)
    image = forms.ImageField(label="Cover Image")

    field_order=['name','address','timeOpens','timeCloses','tags','cuisineTypes','image']

    # An inline class to provide additional information on the form
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Restaurant
        exclude = ('id','manager','starRating','totalReviews',)

#ReviewForm creates reviews from show_restaurant_reviews page
class ReviewForm(forms.ModelForm):
    content = forms.CharField(max_length=1280, label="Content")
    starRating = forms.ChoiceField(choices = STAR_CHOICES, label="Star Rating")

    class Meta:
        model = Review
        exclude = ('id','restaurant','user','date','replyContent')

# LoginForm for user login
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)


class ReplyContentForm(forms.ModelForm):
    replyContent = forms.CharField(max_length=1280, label="Owner's Response")

    class Meta:
        model = Review
        fields = ['replyContent']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields= ('isManager',)

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ('name', 'price', 'restaurant')  

    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        
        self.fields['restaurant'].widget = forms.HiddenInput()

    def save(self, commit=True):
        dish = super().save(commit=False)
        
        if commit:
            dish.save()
        return dish
