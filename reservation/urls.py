from django.contrib import admin
from django.urls import path, include
import food.views
from django.conf import settings
from django.conf.urls.static import static 
from accounts import views
from cart import views 

urlpatterns = [
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('admin/', admin.site.urls),
    path('', food.views.home, name="home"),
    path('<int:food_id>/', food.views.detail, name="detail"), 
    path('accounts/', include('accounts.urls')),
    path('new/', food.views.foodpost, name='new'),
    path('cart/', include('cart.urls')),
    path('<int:food_id>/comment/', food.views.add_comment_to_food, name="comment"),
    path('search/',food.views.search, name="search"),
    path('<int:food_id>/edit/', food.views.edit, name="edit"),
    path('<int:food_id>/delete/', food.views.delete, name="delete")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
