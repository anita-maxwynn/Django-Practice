from django.urls import path
from .views import registration,all_profiles, modify_profile, get_result
urlpatterns = [
    path('register/',registration, name='registration'),
    path('all_profiles/', all_profiles, name='all_profiles'),
    path('modify_profile/<int:pk>/', modify_profile, name='modify_profile'),
    path('get_result/', get_result, name='get_result'),
]
