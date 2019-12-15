from django.contrib import admin
from django.urls import path, include
import food.views
from django.conf import settings
from django.conf.urls.static import static 
from accounts import views as accounts
from text import views as text

# from cart import views 

urlpatterns = [
    path('guide/', food.views.guide, name="guide"),
    path('stream/', food.views.stream, name='stream'),
    # accounts.views 
    path('localaccounts/', include('accounts.urls')),
    path('text/', include('text.urls')),
    # food.views 
    path('<int:food_id>/cart/', food.views.cart, name="cart"),
    path('myCart/', food.views.myCart, name="myCart"),
    path('requested_cart/', food.views.requested_cart, name="requested_cart"),
    path('admin/', admin.site.urls),
    path('', food.views.home, name="home"),
    # path('undo/', food.views.undo, name="undo"),
    path('<int:food_id>/', food.views.detail, name="detail"), 
    # allauth.url 추가시키는거 재확인 요망 
    path('accounts/', include('allauth.urls')),
    path('new/', food.views.foodpost, name='new'),
    path('check/',food.views.checkplz, name="checkplz"),
    path('new/post_retrieve/', food.views.post_retrieve, name="myposts"),
    path('success/', food.views.successPage, name="success"),
    path('requested_cart/past', food.views.past, name="past"),
    path('fail/', food.views.fail, name="fail"),
    path('<int:food_id>/comment/', food.views.add_comment_to_food, name="comment"),
    path('search/',food.views.search, name="search"),
    path('new/post_retrieve/<int:food_id>/edit/', food.views.edit, name="edit"),
    path('new/post_retrieve/delete/<int:food_id>', food.views.delete, name="delete"),
    path('requested_cart/<int:cart2_id>', food.views.checkCanceled, name="checkCanceled"),
    path('requested_cart/done/<int:cart2_id>', food.views.checkDone, name="checkDone"),
    path('manage/<int:customer_id>/', food.views.manage, name="manage"),
    path('customer_list/', food.views.customer_list, name="customer_list"),
    path('cancel/<int:cart_id>', food.views.cancel, name="cancel")
    # path('checking/', food.views.checking, name="checking"),
    # path('requested_cart/res/<int:cart2_id>', food.views.reservation, name="reservation")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
