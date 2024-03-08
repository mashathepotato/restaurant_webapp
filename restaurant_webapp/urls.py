from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from food_advisor import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('food_advisor/', include('food_advisor.urls')),
    path('admin/', admin.site.urls),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
