from django.urls import path
from . import views
urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('home', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('change_password', views.change_password, name='change_password'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password')
]
