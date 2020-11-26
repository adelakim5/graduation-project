from django.urls import path
from . import views

urlpatterns = [
    path('stream/', views.stream, name='stream'),
    path('<int:food_id>/', views.detail, name="detail"), 
    path('new/', views.foodpost, name='new'),
    path('new/post_retrieve/', views.post_retrieve, name="myposts"),
    path('<int:food_id>/comment/', views.add_comment_to_food, name="comment"),
    path('new/post_retrieve/<int:food_id>/edit/', views.edit, name="edit"),
]