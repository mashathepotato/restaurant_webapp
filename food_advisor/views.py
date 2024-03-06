from django.shortcuts import render
from .models import FoodPost, FoodType
from django.db.models import Q
from .forms import UserRegisterForm

def index(request):
    search = request.GET.get('search')
    article_list = FoodPost.objects.all()
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        # 将 search 参数重置为空
        search = ''
    context = {
        'articles': article_list,
        'search': search,
    }
    response = render(request, 'index.html', context)
    return response

def user_login(request):
    response = render(request, 'login.html')
    return response


def user_register(request):
    user_register_form = UserRegisterForm()
    context = {'form': user_register_form}

    response = render(request, 'register.html', context)
    return response

