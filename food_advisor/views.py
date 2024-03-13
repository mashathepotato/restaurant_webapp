from .models import Restaurant 
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib.auth import login, authenticate  
from django.shortcuts import render, redirect
from .forms import ManagerRegistrationForm, UserForm, UserProfileForm, ManagerRegistrationForm, RestaurantEditForm
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

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
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
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

    return render(request, 'register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})

def register_manager(request):
    registered = False
    if request.method == 'POST':
        manager_form = ManagerRegistrationForm(request.POST)
        restaurant_form = RestaurantEditForm(request.POST, request.FILES)

        if manager_form.is_valid() and restaurant_form.is_valid(): # Save the user's form data to the database. 
            manager = manager_form.save()
            restaurant = restaurant_form.save(commit=False)
            restaurant.manager = manager
            restaurant.save()
            registered = True

            login(request, manager)
        else:
            print(manager_form.errors, restaurant_form.errors)
    else:
        manager_form = ManagerRegistrationForm()
        restaurant_form = RestaurantEditForm()

    return render(request, 'food_advisor/register_manager.html',
                  context = {'user_form': manager_form,
                             'profile_form': restaurant_form,
                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request, data=request.POST)
        if form.is_valid:

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
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
    return render(request, 'foodAdvisor/login.html', {'form': form})

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
#def show_restaurant(request, restaurant_id_slug):
    # placeholder view logic here
 #   return render(request, 'food_advisor/show_restaurant.html', {})

#def manage_restaurant(request, restaurant_id_slug):
    # placeholder view logic for managing a restaurant
 #   return render(request, 'food_advisor/manage_restaurant.html', {})

