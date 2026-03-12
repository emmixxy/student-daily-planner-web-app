from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]
# Serve static files first so /static/... isn't caught by the catch-all below
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'planner' / 'static')
urlpatterns += [
    path('', include('planner.urls')),
]
