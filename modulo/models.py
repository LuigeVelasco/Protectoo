from django.db import models
from django.contrib.auth.models import User

class Prefijo(models.Model):
    prefijo = models.CharField(max_length=10)

    def __str__(self):
        return self.prefijo

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    prefijo = models.ForeignKey(Prefijo, on_delete=models.SET_NULL, null=True, blank=True)
    numero = models.CharField(max_length=20)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    bloqueado = models.BooleanField(default=False)
    favorito = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_perfil/', default='default.png', blank=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'
