from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profile/<str:pk>', views.userProfile, name='user_profile'),
    path('update_account', views.updateAccount, name="update_account"),


    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('register', views.registerUser, name="register"),
    path('account', views.userAccount, name="account"),
    path('add_skill', views.addSkill, name="add_skill"),
    path('update_skill/<str:pk>/', views.updateSkill, name="update_skill"),
    path('delete_skill/<str:pk>/', views.deleteSkill, name="delete_skill"),
]
