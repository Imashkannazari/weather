from django.contrib import admin
from django.urls import path
from weather.views import weather_view, handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', weather_view, name='weather_view'),
]

handler404 = 'weather.views.handler404'
