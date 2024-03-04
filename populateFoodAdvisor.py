import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from food_advisor.models import # <MODELS HERE>

def populate():
    # Creates list of dictionaries of mangers to their corresponding
    # restaurant, then adds managers and restaurants.

    restaurant_managers = {
        {'user_name':'Worserspoons Manager',
            'email':'worserspoons@email.com'}:
        {'name': 'Worserspoons',
            'website':'http://pictureofhotdog.com/', 
            'avgStars': 3,
            'total_ratings': 10,
            'address': "8 Murano St, Glasgow G20 7RS",
            'cuisineType': "British",
            'openingTime': 12,
            'closingTime': 23,},

        {'user_name':'Nandos2 Manager',
            'email':'nandos2@email.com'}:
        {'name': 'Gilchrest Savoy (The Wealthiest Man of 1906) Presents: Nandos 2',
            'website':'https://pointerpointer.com/', 
            'avgStars': 4.31,
            'total_ratings': 12,
            'address': "12 Murano St, Glasgow G20 7RS",
            'cuisineType': "South African",
            'openingTime': 16,
            'closingTime': 22,},

        {'user_name':'Groggs Manager',
            'email':'groggs@email.com'}:
        {'name': 'Groggs',
            'website':'https://www.poundland.co.uk/', 
            'avgStars': 1,
            'total_ratings': 5,
            'address': "121 Renfield St, Glasgow G2 3AX",
            'cuisineType': "British",
            'openingTime': 12,
            'closingTime': 13,},}
    
    # Code below goes through mangers dictionary, adds
    # each manager and associated restaurant.

    # WIP BELOW THIS LINE
    
    for manager, res in restaurant_managers.items():
        m = add_manager_user(manager, res['name'], res['website'], res['avgStars'], res['total_ratings'], res['address'], res['cuisineType'], res['openingTime'], res['closingTime'])
        r = add_restaurant(m, res['name'], res['website'], res['avgStars'], res['total_ratings'], res['address'], res['cuisineType'], res['openingTime'], res['closingTime'])
    
    # Print out the categories we have added.

    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')
    
def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views = views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()