from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from food_advisor.models import CuisineType, Restaurant

User = get_user_model()

class ManagerRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',) 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
        return user

class RestaurantEditForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Restaurant Name:")
    address = forms.CharField(max_length=128, help_text="Address")
    timeOpens = forms.TimeField(help_text="Opening Time:")
    timeCloses = forms.TimeField(help_text="Closing Time:")
    tags = forms.CharField(max_length=128, help_text="Tags:")
    cuisineTypes = forms.ModelMultipleChoiceField(queryset=CuisineType.objects.all(),
                                                  label="Cuisine Type",
                                                  widget=forms.CheckboxSelectMultiple,
                                                  help_text="Cuisine Type:",)
    image = forms.ImageField(help_text="Cover Image:")

    # An inline class to provide additional information on the form
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Restaurant
        exclude = ('id','manager','starRating','totalReviews',)