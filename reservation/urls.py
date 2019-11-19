from django.contrib import admin
from django.urls import path, include
import food.views
from django.conf import settings
from django.conf.urls.static import static 
from accounts import views as accounts
# room url때문에 import. 나중에 path형식으로 바꾸는 거 알아보고 수정하자
from django.conf.urls import url

# from cart import views 

urlpatterns = [
    # 채팅 url
    path('index/', food.views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/$', food.views.room, name='room'),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    # alarms.views 
    path('ShareMe', food.views.ShareMe.as_view()),
    path('Alarm', food.views.Alarm.as_view()),
    # accounts.views 
    path('localaccounts/', include('accounts.urls')),
    # food.views 
    path('<int:food_id>/cart/', food.views.cart, name="cart"),
    path('myCart/', food.views.myCart, name="myCart"),
    path('requested_cart/', food.views.requested_cart, name="requested_cart"),
    path('admin/', admin.site.urls),
    path('', food.views.home, name="home"),
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
    path('myCustomer/', food.views.myCustomers, name="myCustomer"),
    path('myCustomer/manage', food.views.manage, name="manage"),
    # path('requested_cart/res/<int:cart2_id>', food.views.reservation, name="reservation")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
