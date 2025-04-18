from django.contrib import admin
from .models import Reseña

@admin.register(Reseña)
class ReseñaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad_visitada', 'correo', 'fecha')
    search_fields = ('nombre', 'ciudad_visitada', 'comentario')
    list_filter = ('fecha',)
