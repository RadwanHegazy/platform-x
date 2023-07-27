from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .settings import ADMIN_URL_NAME
from django.views.static import serve



urlpatterns = [
    path(f'{ADMIN_URL_NAME}/', admin.site.urls),
    path('',include("app.urls")),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
