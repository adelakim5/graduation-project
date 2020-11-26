from django.contrib import admin
from django.urls import path, include
# import food.views
from django.conf import settings
from django.conf.urls.static import static 
# import each apps' views
from accounts import views
from posts import views
from home import views
from carts import views
from text import views

# from cart import views 

urlpatterns = [
    path('localaccounts/', include('accounts.urls')),
    # allauth
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('carts/', include('carts.urls')),
    path('text/', include('text.urls')),
    path('', include('home.urls')),
    path('posts/', include('posts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
