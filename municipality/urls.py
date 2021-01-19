from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('business.urls.api', namespace='BusinessApi')),
]


if settings.DEBUG:
    urlpatterns += static(
        '/media/', document_root=settings.MEDIA_ROOT, show_indexes=True
    )
    urlpatterns += static(
        '/static/', document_root=settings.STATIC_ROOT, show_indexes=True
    )
