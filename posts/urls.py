from django.urls import path
from . import views

urlpatterns = [
    path('stream/', views.stream, name='stream'),
    path('<int:food_id>/', views.detail, name="detail"), 
    path('writeNewPost/', views.writeNewPost, name='writeNewPost'),
    path('viewMyPostList/', views.viewMyPostList, name="viewMyPostList"),
    path('<int:food_id>/comment/', views.addComments, name="addComments"),
    path('edit/<int:food_id>/', views.edit, name="edit"),
    path('delete/<int:food_id>', views.delete, name="delete"),
]