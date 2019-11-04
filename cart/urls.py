from django.urls import path
from .views import *

urlpatterns=[
    # 장바구니에 상품 후가하는 페이지로 이동하는 경로
    path('<int:food_id>/add', add_food, name="add_food"),
    # 장바구니에서 상품 삭제하는 view로 이동하는 경로
    path('<int:food_id>/remove', remove_food, name="remove_food"),
    # 장바구니 상세정보가 조회되는 페이지로 이동하는 경로
    path('detail/', cart_detail, name="cart_detail"),

]