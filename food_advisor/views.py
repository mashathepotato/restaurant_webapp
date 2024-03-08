from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Restaurant, Review, User 
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import login, authenticate  
from django.shortcuts import render, redirect
from .forms import ManagerRegistrationForm
from django.shortcuts import render, get_object_or_404

def index(request):
    restaurants = Restaurant.objects.all()  # Get all restaurants
    return render(request, 'food_advisor/index.html', {'restaurants': restaurants})


def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()
            
            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            # Now we save the UserProfile model instance.
            profile.save()
            
            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    # Render the template depending on the context.
    return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_signin(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('food_advisor:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'food_advisor/login.html')

def registerUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('food_advisor:index')
    else:
        form = UserCreationForm()
    return render(request, 'food_advisor/register.html', {'form': form})

def registerOwner(request):
    if request.method == 'POST':
        form = ManagerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('food_advisor:index')
    else:
        form = ManagerRegistrationForm()
    return render(request, 'food_advisor/owner.html', {'form': form})

def password_reset(request):
    return render(request, 'food_advisor/password_reset.html')

def nothing(request):
    return render(request, 'nothing.html')
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