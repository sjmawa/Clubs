from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('core.urls')),
    path('clubs/', include('clubs.urls')),      # example: home goes to clubs app
    path('events/',include('events.urls')),
    path('users/',include('users.urls')),
]
urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
