from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_view, name='index'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]
