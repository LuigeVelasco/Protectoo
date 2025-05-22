from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('crear/', views.crear_contacto, name='crear_contacto'),
    path('detalle/<int:id>/', views.detalle_contacto, name='detalle_contacto'),
    path('login/', auth_views.LoginView.as_view(template_name='modulo/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('detalle/<int:id>/', views.detalle_contacto, name='detalle_contacto'),
    path('toggle_favorito/<int:id>/', views.toggle_favorito, name='toggle_favorito'),
    path('toggle_bloqueado/<int:id>/', views.toggle_bloqueado, name='toggle_bloqueado'),
    path('editar/<int:contacto_id>/', views.editar_contacto, name='editar_contacto'),
    path('eliminar/<int:contacto_id>/', views.eliminar_contacto, name='eliminar_contacto'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil_view, name='perfil_usuario'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),
]
