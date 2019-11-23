from django.urls import path, include
from . import views

urlpatterns = [
    path('stream/', views.stream, name='stream'),
    path('stream/send', views.send_notification, name='send'),
]