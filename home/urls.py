from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('guide/', views.guide, name="guide"),
    path('search/',views.search, name="search"),
]