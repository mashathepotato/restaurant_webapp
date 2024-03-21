import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Restaurant, Review, User, Dish, UserProfile, CuisineType
from django.contrib.auth.forms import  AuthenticationForm 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import DishForm, ManagerRegistrationForm, UserForm, UserProfileForm, ManagerRegistrationForm, RestaurantEditForm, ReviewForm, ReplyContentForm
from django.contrib.auth.forms import UserCreationForm  
from django.shortcuts import render, get_object_or_404

def index(request):
    context_dict = {}
    cuisine_types = CuisineType.objects.all()
    search_query = request.GET.get('search', '')
    filter_query = request.GET.get('filter', '')
    if search_query:
        restaurants = Restaurant.objects.filter(name__icontains=search_query)
        context_dict['prev_search'] = search_query
    elif filter_query and (filter_query != "None"):
        restaurants = Restaurant.objects.filter(cuisineTypes__name__icontains=filter_query)
        context_dict['prev_filter'] = filter_query
    else:
        restaurants = Restaurant.objects.all()
    for restaurant in restaurants:
        restaurant.full_stars = range(restaurant.getIntegerStars())
        restaurant.empty_stars = range(5 - restaurant.getIntegerStars())
    cuisine_types_text = []
    for cuisine_type in cuisine_types:
        cuisine_types_text.append(cuisine_type.name)
    context_dict = context_dict | {'restaurants': restaurants, 'cuisine_types': cuisine_types_text} 
    return render(request, 'food_advisor/index.html', context_dict)

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

@login_required
def manage_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, manager__user=request.user)
    dishes = Dish.objects.filter(restaurant=restaurant)
    
    if request.method == "POST":
        form = RestaurantEditForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            
            return redirect('food_advisor:show_restaurant', restaurant_id_slug=restaurant.id)
    else:
        form = RestaurantEditForm(instance=restaurant)

    context_dict = {
    'restaurant_form': form,  
    'restaurant': restaurant,
    'dishes': dishes,
}
    return render(request, 'food_advisor/manage_restaurant.html', context_dict)

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
            restaurant_form.instance.manager = manager_profile
            restaurant_form.save()
            registered = True

            login(request, manager)
            return redirect('food_advisor:index')
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
                    messages.error(request, "Your foodAdvisor account is disabled.")
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
    
def show_restaurant(request, restaurant_id_slug):
    context_dict = {}

    try:
        # Get restaurant from id, if not exists, throw error.
        restaurant = Restaurant.objects.get(id=restaurant_id_slug)
        restaurant.full_stars = range(restaurant.getIntegerStars())
        restaurant.empty_stars = range(5 - restaurant.getIntegerStars())
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
        restaurant = Restaurant.objects.get(id=restaurant_id_slug)

        reviews = Review.objects.filter(restaurant=restaurant)

        context_dict['reviews'] = reviews
        context_dict['restaurant'] = restaurant
        context_dict['restaurant_id']=restaurant_id_slug

        userNotReviewed = True
        for review in reviews:
            if review.user == request.user:
                userNotReviewed = False
        context_dict['userNotReviewed'] = userNotReviewed

        if request.method == 'POST' and userNotReviewed:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.restaurant = restaurant
                review.user = request.user
                review.save()
                new_total_stars = restaurant.totalReviews * restaurant.starRating
                new_total_reviews = restaurant.totalReviews
                new_total_stars += int(review_form.cleaned_data['starRating'])
                new_total_reviews += 1
                restaurant.totalReviews = new_total_reviews
                restaurant.starRating = new_total_stars / new_total_reviews
                restaurant.save()
                return redirect(reverse('food_advisor:show_restaurant_reviews', kwargs={'restaurant_id_slug':restaurant_id_slug}))  
            else:
                print(review_form.errors)
        else:
            review_form = ReviewForm()
            context_dict['review_form'] = review_form


    except Restaurant.DoesNotExist:
        context_dict['restaurant'] = None
        context_dict['reviews'] = None

    return render(request, 'food_advisor/show_restaurant_reviews.html', context=context_dict)

def review_reply(request, review_id, restaurant_id_slug):
    context_dict = {}
    try:
        review = Review.objects.get(id=review_id)
        restaurant = Restaurant.objects.get(id=restaurant_id_slug)
        context_dict['review'] = review
        context_dict['restaurant_id']=restaurant_id_slug

        if request.method == 'POST':
            review_form = ReplyContentForm(request.POST, instance=review)

            if review_form.is_valid():
                review.save()
                return redirect(reverse('food_advisor:show_restaurant_reviews', kwargs={'restaurant_id_slug':review.restaurant.id}))  
            else:
                print(review_form.errors)
        else:
            review_form = ReplyContentForm(instance=review)
            context_dict['review_form'] = review_form

    except Review.DoesNotExist:
        context_dict['review'] = None

    return render(request, 'food_advisor/review_reply.html', context=context_dict)


@login_required
def manage_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, manager__user=request.user)
    dishes = Dish.objects.filter(restaurant=restaurant)
    
    if request.method == "POST":
        form = RestaurantEditForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            
            return redirect('food_advisor:show_restaurant', restaurant_id_slug=restaurant.id)
    else:
        form = RestaurantEditForm(instance=restaurant)

    context_dict = {
    'restaurant_form': form,  
    'restaurant': restaurant,
    'dishes': dishes,
}
    return render(request, 'food_advisor/manage_restaurant.html', context_dict)


@login_required
def add_dish_ajax(request, restaurant_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == "POST":
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            dish = form.save(commit=False)
            dish.restaurant = restaurant
            dish.save()
            return JsonResponse({"id": dish.id, "name": dish.name, "price": dish.price}, status=200)
        else:
            return JsonResponse({"error": form.errors.as_json()}, status=400)
    else:
        return JsonResponse({"error": "Not an AJAX request"}, status=400)

@login_required
def delete_dish_ajax(request, dish_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'DELETE':
        dish = get_object_or_404(Dish, id=dish_id, restaurant__manager__user=request.user)
        dish.delete()
        return JsonResponse({"message": "Dish deleted successfully"}, status=200)
    else:
        return JsonResponse({"error": "Not an AJAX request"}, status=400)
