from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('toggle-like/<int:car_id>/', toggle_like, name='toggle_like'),
    path('get-likes/<int:car_id>/', get_likes, name='get_likes'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
    path('feedback/', feedback, name='feedback'),
]