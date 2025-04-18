from django.contrib import admin
from django.urls import path, include
from users.views import home_view 
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Enlaza las rutas de la app users
    path('', home_view, name='home'),  # Página principal
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 