from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from weather.views import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('weather.urls', namespace='weather')),
]

# Add handler404
handler404 = 'weather.views.handler404'

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
