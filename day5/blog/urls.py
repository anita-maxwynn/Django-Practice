# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('create/', views.create, name='create_blog'),
    path('update/<int:pk>/', views.update, name='update_blog'),
    path('delete/<int:pk>/', views.delete, name='delete_blog'),
]
