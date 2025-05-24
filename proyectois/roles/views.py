from pyexpat.errors import messages
from django.shortcuts import render, redirect
from django.db import connection


def listar_roles(request):
    with connection.cursor() as c:
        c.callproc('sp_listar_roles')
        roles = c.fetchall()
    return render(request, 'roles/listar.html', {'roles': roles})

def crear_rol(request):
    if request.method=='POST':
        c=connection.cursor()
        c.callproc('sp_registrar_rol', [request.POST['nombre'], request.POST['descripcion']])
        return redirect('listar_roles')
    return render(request, 'roles/crear.html')

def asignar_rol(request):
    if request.method == 'POST':
        usuario_id = request.POST['usuario_id']
        rol_id     = request.POST['rol_id']
        with connection.cursor() as cursor:
            cursor.callproc('sp_asignar_rol', [usuario_id, rol_id])
        messages.success(request, 'Rol asignado correctamente')
        return redirect('roles:listar_roles')

    # GET: cargar usuarios
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_usuarios')
        usuarios = cursor.fetchall()

    # GET: cargar roles
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_roles')
        roles = cursor.fetchall()

    return render(request, 'roles/asignar.html', {
        'usuarios': usuarios,
        'roles': roles
    })