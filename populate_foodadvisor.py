import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'restaurant_webapp.settings')
BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
import django
from django.core.files import File
django.setup()
from food_advisor.models import User, Restaurant, Review, Dish, UserProfile, CuisineType
import datetime

def populate():
    cuisine_types = ['Indian','Chinese','Italian','French','British','American']
    for type in cuisine_types:
        c = CuisineType.objects.get_or_create(name=type)[0]
        c.name=type
        c.save()

    ihop_dishes = [
        {'name':'Pancake stack','price':6.5},
        {'name':'Fruit salad','price':3.5},
        {'name':'Belgian waffles','price':5},
        {'name':'Grits','price':4},
        {'name':'Egg','price':3}
    ]

    subway_dishes = [
        {'name':'BLT','price':4},
        {'name':'Veggie Delite','price':4}
    ]

    greggs_dishes = [
        {'name':'Sausage Roll','price':1.2},
        {'name':'Cheese Bake','price':2.35}
    ]

    users = [
        {'username':'Sarah','email':'email@blank.com'},
        {'username':'Donahue','email':'road@runner.com'},
        {'username':'Terry','email':'user@use.com'},
        
    ]

    ihop_reviews = [
        {'username':'Sarah','content':'Pancakes were great', 'stars':4},
        {'username':'Donahue','content':'Service was slow', 'stars':2},
        {'username':'Terry','content':'Grits were delicious','stars':5}
    ]

    subway_reviews = [
        {'username':'Sarah','content':'Sandwich was cold when I got it', 'stars':1},
        {'username':'Donahue','content':'Workers were rude but good sandwich', 'stars':3},
        {'username':'Terry','content':'Thumbs up','stars':3}
    ]

    greggs_reviews = [
        {'username':'Donahue','content':'Queue of students is long at lunch time. Friendly staff','stars':3},
        {'username':'Terry','content':'Tasty lunch good price','stars':4},
    ]

    restaurant_managers = [
        [{'username':'iHopManager',
            'email':'ihop@manager.com',
            'restaurant':'iHop'},
        {'name':'iHop',
            'dishes': ihop_dishes, 
            'reviews': ihop_reviews, 
            'address': '61 Fake Dr',
            'Manager':'iHopManager',
            'open':datetime.time(7,0),
            'close':datetime.time(0,0),
            'starRating':3.66666,
            'totalReviews':3,
            'cuisineTypes':['American'],
            'imageName':'iHop.jpg'}],

        [{'username':'SubwayManager',
            'email':'subway@manager.com',
            'restaurant':'Subway'},
        {'name':'Subway',
            'dishes': subway_dishes, 
            'reviews': subway_reviews, 
            'address':'9-11 Merkland St, Partick, Glasgow, UK',
            'Manager':'SubwayManager',
            'open':datetime.time(7,0),
            'close':datetime.time(19,0),
            'starRating':2.33333,
            'totalReviews':3,
            'cuisineTypes':['American'],
            'imageName':'subway.webp'}],

        [{'username':'GreggsManager',
            'email':'greggs@manager.com',
            'restaurant':'Greggs'},
          {'name':'Greggs',
            'dishes': greggs_dishes, 
            'reviews': greggs_reviews, 
            'address':'77 Mirage Blvd, Barnegat, NJ, USA',
            'Manager':'GreggsManager',
            'open':datetime.time(5,0),
            'close':datetime.time(21,0),
            'starRating':3.5,
            'totalReviews':2,
            'cuisineTypes':['British'],
            'imageName':'greggs.jpg'}]
    ]

    for user in users:
        add_user(user['username'], user['email'])
        
    for manager, rest_data in restaurant_managers:
        manager_user = add_user(manager['username'], manager['email'])
        manager_user.isManager=True
        manager_user.save()
        r = add_restaurant(rest_data['name'], rest_data['address'], manager_user, rest_data['imageName'], rest_data['starRating'], rest_data['totalReviews'])
        for d in rest_data['dishes']:
            add_dishes(r, d['name'], d['price'])
        for c in rest_data['cuisineTypes']:
            add_cuisineType(r, c)
        for s in rest_data['reviews']:
            add_review(r, s['username'], s['content'], s['stars'])

def add_cuisineType(rest, name):
    type = CuisineType.objects.get(name=name)
    type.save()
    rest.cuisineTypes.add(type)

def add_review(rest, username, content, stars):
    user = User.objects.get(username=username)
    r = Review.objects.get_or_create(restaurant=rest, user=user, content=content)[0]
    r.user=user
    r.restaurant=rest
    r.content=content
    r.starRating=stars
    r.save()
    return r

def add_dishes(rest, name, price):
    d = Dish.objects.get_or_create(restaurant=rest,name=name, price=price)[0]
    d.restaurant=rest
    d.name=name
    d.price=price
    d.save()
    return d

def add_restaurant(name, address, manager, imageName, starRating=1.0, totalReviews=0, ):
    r = Restaurant.objects.get_or_create(name=name, address=address, manager=manager)[0]
    r.name=name
    r.address=address
    r.manager=manager
    r.starRating=starRating
    r.totalReviews=totalReviews
    r.tags = "Tag1, Tag2"
    r.save()
    file_path = os.path.join(BASE_DIR,"population_resources",imageName)
    r.image.save(imageName, File(open(file_path,'rb')))
    return r
    
def add_user(username, email):
    u = User.objects.get_or_create(username=username, email=email)[0]
    u.username=username
    u.email=email
    u.save()
    p = UserProfile.objects.get_or_create(user=u)[0]
    p.user=u
    p.save()
    return p

if __name__ == '__main__':
    print('Starting food_advisor population script...')
    populate()