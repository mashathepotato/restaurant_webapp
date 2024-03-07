from .models import Restaurant, Review, User 
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import login, authenticate  
from django.shortcuts import render, redirect
from .forms import ManagerRegistrationForm, UserForm, UserProfileForm, RestaurantForm, ManagerForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
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
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
            login(request, user)
            return redirect('foodAdvidor: index')
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
        manager_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST)

        if manager_form.is_valid() and restaurant_form.is_valid(): # Save the user's form data to the database. 
            manager = manager_form.save()
            manager.set_password(manager.password)
            manager.save()
            restaurant = restaurant_form.save(commit=False)
            restaurant.user = manager
            if 'picture' in request.FILES:
                restaurant.picture = request.FILES['picture']
            
            restaurant.save()
            registered = True
        else:
            print(manager_form.errors, restaurant_form.errors)
    else:
        manager_form = ManagerForm()
        restaurant_form = RestaurantForm()

    return render(request, 'foodAdvisor/register_manager.html',
                  context = {'user_form': manager_form,
                             'profile_form': restaurant_form,
                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
                return redirect(reverse('foodAdvisor:index'))
            else:
                return HttpResponse("Your foodAdvisor account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
# No context variables to pass to the template system, hence the # blank dictionary object...
        return render(request, 'foodAdvisor/login.html')

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

