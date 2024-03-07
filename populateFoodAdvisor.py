import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_webapp.settings')

import django
django.setup()
from django.contrib.auth.models import User
from food_advisor.models import Restaurant, Review, Dish

def populate():
    # Creates list of dictionaries of mangers to their corresponding
    # restaurant, then adds managers and restaurants.

    restaurant_managers = [
        [
            {'username':'Worserspoons Manager',
                'email':'worserspoons@email.com',
                'password':'test'},
            {'name': 'Worserspoons',
                'website':'http://pictureofhotdog.com/', 
                'avg_stars': 3,
                'total_ratings': 10,
                'address': "8 Murano St, Glasgow G20 7RS",
                'cuisineType': "British",
                # 'timeOpens': 12,
                # 'timeCloses': 23,
                'tags':"Tag1, Tag2, Tag3"}
        ],

        [
            {'username':'Nandos2 Manager',
                'email':'nandos2@email.com',
                'password':'test'},
            {'name': 'Gilchrest Savoy (The Wealthiest Man of 1906) Presents: Nandos 2',
                'website':'https://pointerpointer.com/', 
                'avg_stars': 4.31,
                'total_ratings': 12,
                'address': "12 Murano St, Glasgow G20 7RS",
                'cuisineType': "South African",
                # 'timeOpens': 16,
                # 'timeCloses': 22,
                'tags':"Tag1, Tag2, Tag3"}
        ],

        [
            {'username':'Groggs Manager',
                'email':'groggs@email.com',
                'password':'test'},
            {'name': 'Groggs',
                'website':'https://www.poundland.co.uk/', 
                'avg_stars': 1,
                'total_ratings': 5,
                'address': "121 Renfield St, Glasgow G2 3AX",
                'cuisineType': "British",
                # 'timeOpens': 12,
                # 'timeCloses': 13,
                'tags':"Tag1, Tag2, Tag3"}
        ]
    ]
    
    # Code below goes through mangers list, adds
    # each manager and associated restaurant.
    
    for items in restaurant_managers:
        manager = items[0]
        res = items[1]
        m = add_user(manager['username'], manager['email'], manager['password'])
        r = add_restaurant(m, res['name'], res['website'], res['avg_stars'], res['total_ratings'], res['address'], res['cuisineType'])
    
    # Print out what we have added
        
    add_user("Normal Guy", "normal@guy.com", "test")

    for u in User.objects.all():
        print(u)

    for r in Restaurant.objects.all():
        print(r)
    
def add_user(username, email, password):
    u = User.objects.get_or_create(
        username=username,
        email=email,
        password=password)[0]
    u.save()
    return u

def add_restaurant(manager, name, website, avg_stars, total_ratings, address, cuisineType):
    r = Restaurant.objects.get_or_create(
        manager=manager,
        name=name,
        url=website,
        avg_stars=avg_stars,
        total_ratings=total_ratings,
        address=address,
        cuisineType=cuisineType)[0]
    r.save()
    return r



if __name__ == '__main__':
    print('Starting FoodAdvisor population script...')
    populate()