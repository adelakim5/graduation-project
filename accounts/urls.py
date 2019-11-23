from django.urls import path, include
from . import views
# from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('profile/', views.profilepage, name='profile'),
    path('profile/profile_detail', views.user_profile, name="profile_detail"),
    # path('profile/update/', views.update, name='update'),
    path('oauth/', views.oauth, name="oauth"),
    # path('hello/', views.friends, name='hello'),
    path('profile/user_delete', views.user_delete, name="user_delete"),
] 