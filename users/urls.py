from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profile/<str:pk>', views.userProfile, name='user_profile'),
]
