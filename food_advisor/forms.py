from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile


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
        user.is_manager = True  # Ensure your User model supports this attribute
        if commit:
            user.save()
        return user

class RestaurantEditForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Restaurant Name:")
    address = forms.CharField(max_length=128, help_text="Address")
    timeOpens = forms.TimeField(help_text="Opening Time:")
    timeCloses = forms.TimeField(help_text="Closing Time:")
    tags = forms.CharField(max_length=128, help_text="Tags:")
    cuisineTypes = forms.ModelMultipleChoiceField(CuisineType.objects.all(),
                                                  label="Cuisine Type",
                                                  widget=forms.CheckboxSelectMultiple,
                                                  help_text="Cuisine Type:")
    image = forms.ImageField(help_text="Cover Image:")

    # An inline class to provide additional information on the form
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Restaurant
        exclude = ('id','manager','starRating','totalReviews',)

# LoginForm for user login
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields= ('bio', 'website', 'picture')