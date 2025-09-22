from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static # Keep this for clarity, though its use for media is conditional
from django.views.static import serve 
from app.views import ckeditor_upload_to_webp
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('ckeditor/upload/', ckeditor_upload_to_webp, name='ckeditor_upload'),
    path('', include('app.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This block is for when DEBUG is True (Django's default static file serving)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
