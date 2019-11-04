from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('login/', views.login, name="login"),
    #path('', include('allauth.urls')),
    path('login/', include('allauth.urls')),
    path('signup/', views.CreateUserView.as_view(), name="signup"),
    path('signup_done', views.RegisteredView.as_view(), name='signup_done'),
    path('logout/', views.logout, name="logout"),
    path('profile/<int:pk>', login_required(views.ProfileView.as_view()), name='profile'),
    path('profile_update/', login_required(views.ProfileUpdateView.as_view()), name="profile_update"),
    # path('update/', views.update, name='update'),
    path('oauth/', views.oauth, name="oauth"),
    # path('user_delete', views.user_delete, name="user_delete"),
]