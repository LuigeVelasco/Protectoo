from django.contrib import admin
from .models import Contacto, Prefijo

@admin.register(Prefijo)
class PrefijoAdmin(admin.ModelAdmin):
    list_display = ('id', 'prefijo')
    search_fields = ('prefijo',)

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'prefijo', 'numero', 'autor', 'bloqueado', 'favorito')
    list_filter = ('bloqueado', 'favorito', 'autor', 'prefijo')
    search_fields = ('nombre','prefijo__prefijo', 'numero', 'autor__username')
