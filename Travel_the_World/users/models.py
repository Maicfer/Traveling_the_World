from django.db import models
from django.contrib.auth.models import User

from django.db import models

from django.db import models

class Destino(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.URLField(default='https://via.placeholder.com/800x600')  # Imagen como URL
    enlace = models.URLField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} - {self.pais}"


    
class Reseña(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    ciudad_visitada = models.CharField(max_length=100)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    
class Meta:
    ordering = ['-fecha'] 

    def __str__(self):
        return f"{self.nombre} - {self.destino}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    document_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return f'Perfil de {self.user.username}'