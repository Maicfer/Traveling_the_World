from django.urls import path
from . import views  
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),  # Vista de perfil
    path('update/', views.update_profile_view, name='update_profile'),  # Edición de usuario
    path('change-password/', views.change_password_view, name='change_password'),  # Cambio de clave
    path('update-email/', views.change_email_view, name='update_email'), # Actualización de email
    path('buscar-vuelos/', views.buscar_vuelos, name='buscar_vuelos'),
    path('destinos/', views.destinos_view, name='destinos'),
    path('destinos-texto/', views.mostrar_destinos),
    path('cargar_destinos/', views.cargar_datos_si_es_necesario ),
    path('mas_visitados/', views.mas_visitados, name='mas_visitados'),
    path('vuelos/', views.vuelos, name='consultar_vuelos'),
    path('hoteles/', views.hoteles, name='consultar_hoteles'),
    path('paquetes/', views.paquetes, name='consultar_paquetes'),
    path('reseñas/', views.reseñas_view, name='reseñas'),


]
