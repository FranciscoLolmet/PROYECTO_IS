from django.shortcuts import render, redirect
from django.db import connection

def listar_vacaciones(request):
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_vacaciones')
        vacs = cursor.fetchall()
    return render(request, 'vacaciones/listar.html', {'vacaciones': vacs})


def registrar_vacacion(request):
    if request.method=='POST':
        data = [
            request.POST['empleado_id'],
            request.POST['fecha_inicio'],
            request.POST['fecha_fin'],
            request.POST['dias_disfrutados'],
            request.POST['periodo'],
        ]
        with connection.cursor() as cursor:
            cursor.callproc('sp_registrar_vacaciones', data)
        return redirect('vacaciones:listar_vacaciones')
    # cargar empleados para select
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_empleados')
        empleados = cursor.fetchall()
    return render(request, 'vacaciones/registrar.html', {'empleados': empleados})