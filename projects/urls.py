from django.urls import path
from . import views


urlpatterns = [
    path('projects', views.projects, name='projects'),
    path('projects/<str:pk>', views.project_detail, name='project'),
    path('add', views.add_project, name='add'),
    path('update/<str:pk>', views.update_project, name='update'),
    path('delete/<str:pk>', views.delete_project, name='delete'),

]
