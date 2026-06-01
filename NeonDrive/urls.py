from django.contrib import admin
from django.urls import include, path

from main.views import toggle_like, get_likes

urlpatterns = [
    path('toggle-like/<int:car_id>/', toggle_like, name='toggle_like'),
    path('get-likes/<int:car_id>/', get_likes, name='get_likes'),  # ДОБАВИТЬ ЭТУ СТРОЧКУ
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]