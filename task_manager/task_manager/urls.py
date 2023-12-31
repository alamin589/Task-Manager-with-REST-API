from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tasks.views import UserLogin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('', UserLogin.as_view(), name='user-login'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
