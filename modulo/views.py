from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from .models import Contacto
from .forms import ContactoForm, RegistroUsuarioForm, PerfilForm
from django.contrib.auth import login
from .forms import PerfilForm, FotoPerfilForm
from .models import Perfil


@login_required(login_url='login')  # Asegura que el usuario esté logueado
def index(request):
    filtro = request.GET.get('filtro', 'todos')
    buscar = request.GET.get('buscar', '')

    contactos = Contacto.objects.filter(autor=request.user)

    if buscar:
        contactos = contactos.filter(nombre__icontains=buscar)

    if filtro == 'favoritos':
        contactos = contactos.filter(favorito=True)
    elif filtro == 'bloqueados':
        contactos = contactos.filter(bloqueado=True)

    contactos = contactos.order_by('nombre')  # orden alfabético

    return render(request, 'modulo/index.html', {
        'contactos': contactos,
        'filtro': filtro
    })




@login_required
def crear_contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.autor = request.user
            contacto.save()
            return redirect('index')
    else:
        form = ContactoForm()
    return render(request, 'modulo/crear_contacto.html', {'form': form})

@login_required
def detalle_contacto(request, id):
    contacto = get_object_or_404(Contacto, id=id, autor=request.user)
    return render(request, 'modulo/detalle_contacto.html', {'contacto': contacto})

from django.shortcuts import redirect, get_object_or_404
from .models import Contacto
from django.contrib.auth.decorators import login_required

@login_required
def toggle_favorito(request, id):
    contacto = get_object_or_404(Contacto, id=id, autor=request.user)
    if request.method == 'POST':
        contacto.favorito = not contacto.favorito
        contacto.save()
    return redirect('index')

@login_required
def toggle_bloqueado(request, id):
    contacto = get_object_or_404(Contacto, id=id, autor=request.user)
    if request.method == 'POST':
        contacto.bloqueado = not contacto.bloqueado
        contacto.save()
    return redirect('index')

@login_required
def editar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id, autor=request.user)
    if request.method == 'POST':
        form = ContactoForm(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ContactoForm(instance=contacto)
    return render(request, 'modulo/editar_contacto.html', {'form': form, 'contacto': contacto})

@login_required
def eliminar_contacto(request, contacto_id):
    contacto = get_object_or_404(Contacto, id=contacto_id, autor=request.user)
    if request.method == 'POST':
        contacto.delete()
        return redirect('index')
    return render(request, 'modulo/eliminar_confirmacion.html', {'contacto': contacto})

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('index')
    else:
        form = RegistroUsuarioForm()
    
    return render(request, 'modulo/registro.html', {'form': form})


@login_required
def perfil_view(request):
    perfil, creado = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        foto_form = FotoPerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid() and foto_form.is_valid():
            form.save()
            foto_form.save()  # Guarda la foto de perfil
            return redirect('perfil_usuario')  # Redirige a la vista del perfil
    else:
        form = PerfilForm(instance=request.user)
        foto_form = FotoPerfilForm(instance=perfil)

    return render(request, 'modulo/perfil.html', {
        'form': form,
        'foto_form': foto_form,
        'perfil': perfil
    })


@login_required
def perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        foto_form = FotoPerfilForm(request.POST, request.FILES, instance=request.user.perfil)
        if form.is_valid() and foto_form.is_valid():
            form.save()
            foto_form.save()
            return redirect('index')
    else:
        form = PerfilForm(instance=request.user)
        foto_form = FotoPerfilForm(instance=request.user.perfil)

    return render(request, 'modulo/perfil.html', {
        'form': form,
        'foto_form': foto_form,
    })

@login_required
def editar_perfil_view(request):
    user = request.user
    perfil, creado = Perfil.objects.get_or_create(usuario=user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            if 'foto' in request.FILES:
                perfil.foto = request.FILES['foto']
                perfil.save()
            return redirect('perfil_usuario')
    else:
        form = PerfilForm(instance=user)

    return render(request, 'modulo/perfil.html', {'form': form, 'perfil': perfil})