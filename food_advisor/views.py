from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Restaurant, Review, User, Dish
from django.contrib.auth.forms import  AuthenticationForm 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ManagerRegistrationForm, UserForm, UserProfileForm, ManagerRegistrationForm, RestaurantEditForm
from django.shortcuts import render, get_object_or_404

def index(request):
    restaurants = Restaurant.objects.all()  # Get all restaurants
    return render(request, 'food_advisor/index.html', {'restaurants': restaurants})


def register_user(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid(): # Save the user's form data to the database. 
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.isManager = False
            profile.save()
            registered = True
            login(request, user)

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('food_advisor:index')
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'food_advisor/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})

def register_manager(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        manager_profile_form = UserProfileForm(request.POST)
        restaurant_form = RestaurantEditForm(request.POST, request.FILES)

        if user_form.is_valid() and manager_profile_form.is_valid() and restaurant_form.is_valid(): # Save the user's form data to the database. 
            manager = user_form.save()
            manager_profile = manager_profile_form.save(commit=False)
            manager_profile.user = manager
            manager_profile.isManager = True
            manager_profile.save()
            restaurant = restaurant_form.save(commit=False)
            restaurant.manager = manager_profile
            restaurant.save()
            registered = True

            login(request, manager)
        else:
            print(user_form.errors, manager_profile_form.errors,restaurant_form.errors)
    else:
        user_form = UserForm()
        manager_profile_form = UserProfileForm()
        restaurant_form = RestaurantEditForm()

    return render(request, 'food_advisor/owner.html',
                  context = {'user_form': user_form,
                             'profile_form': manager_profile_form,
                             'restaurant_form': restaurant_form,
                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request)
        if form.is_valid:

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('food_advisor:index'))
                else:
                    messages(request, "Your foodAdvisor account is disabled.")
            else:
                messages.error(request, "Invalid login details.")
        else:
            messages.error(request, form.errors)
    else:
        form = AuthenticationForm()
                                                # No context variables to pass to the template system, hence the # blank dictionary object...
    return render(request, 'food_advisor/login.html', {'form': form})

def nothing(request):
    return render(request, 'nothing.html')

@login_required
def user_logout(request):
    # Since we know user is logged in, we can simply log them out.
    logout(request)
    return redirect(reverse('food_advisor:index'))

#@login_required
#def restricted(request):
#    return render(request, 'rango/restricted.html')

#@login_required
#def user_logout(request):
 #   logout(request)
  #  return redirect('rango:index')

# A helper method
#def get_server_side_cookie(request, cookie, default_val=None):
 #   val = request.session.get(cookie)
  #  if not val:
   #     val = default_val
#return val

    
def show_restaurant(request, restaurant_id_slug):
    context_dict = {}

    try:
        # Get restaurant from id, if not exists, throw error.
        restaurant = Restaurant.objects.get(id=restaurant_id_slug)

        # Retrieve all dishes from restaurant.
        dishes = Dish.objects.filter(restaurant=restaurant)

        context_dict['dishes'] = dishes
        context_dict['restaurant'] = restaurant
        context_dict['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY

    except Restaurant.DoesNotExist:
        # If don't find restaurant, do nothing.
        context_dict['restaurant'] = None
        context_dict['dishes'] = None
        context_dict['google_maps_api_key'] = None

    # Render response and return it to the client
    return render(request, 'food_advisor/show_restaurant.html', context=context_dict)

def show_restaurant_reviews(request, restaurant_id_slug):
    context_dict = {}

    try:
        # Get restaurant from id, if not exists, throw error.
        restaurant = Restaurant.objects.get(id=restaurant_id_slug)

        # Retrieve all reviews from restaurant.
        reviews = Review.objects.filter(restaurant=restaurant)

        context_dict['reviews'] = reviews
        context_dict['restaurant'] = restaurant

    except Restaurant.DoesNotExist:
        # If don't find restaurant, do nothing.
        context_dict['restaurant'] = None
        context_dict['reviews'] = None

    # Render response and return it to the client
    return render(request, 'food_advisor/show_restaurant_reviews.html', context=context_dict)

def manage_restaurant(request, restaurant_id_slug):
    try:
        restaurant = Restaurant.objects.get(id=restaurant_id_slug)
    except Restaurant.DoesNotExist:
        restaurant = None

    if restaurant is None:
        return redirect('/food_advisor/')
    
    form = RestaurantEditForm(instance=restaurant)

    if request.method == "POST":
        form = RestaurantEditForm(request.POST, request.FILES, instance=restaurant)

        if form.is_valid():
            form.save()
            return redirect(reverse('food_advisor:show_restaurant', kwargs={'restaurant_id_slug':restaurant_id_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'restaurant':restaurant}
    return render(request, 'food_advisor/manage_restaurant.html', context_dict)

#def manage_restaurant(request, restaurant_id_slug):
    # placeholder view logic for managing a restaurant
 #   return render(request, 'food_advisor/manage_restaurant.html', {})
