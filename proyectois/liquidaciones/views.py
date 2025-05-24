from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

from datetime import datetime

def listar_liquidaciones(request):
    # Cargar empleados para filtro
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_empleados')
        empleados = cursor.fetchall()

    selected = request.GET.get('empleado_id', '')
    fecha   = request.GET.get('fecha_baja', '')

    # Llamar SP para listar liquidaciones completas
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_liquidaciones')
        rows = cursor.fetchall()

    # Filtrar cliente y fecha
    liquidaciones = []
    for r in rows:
        emp_id = str(r[1])
        fec    = r[2].strftime('%Y-%m-%d')
        if selected and emp_id != selected:
            continue
        if fecha and fec != fecha:
            continue
        liquidaciones.append(r)

    return render(request, 'liquidaciones/listar.html', {
        'liquidaciones': liquidaciones,
        'empleados': empleados,
        'selected_id': selected,
        'selected_fecha': fecha,
    })

from django.utils import timezone

def generar_liquidacion(request):
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_empleados')
        empleados = cursor.fetchall()

    if request.method == 'POST':
        try:
            emp_id = int(request.POST['empleado_id'])
            fecha_baja = request.POST['fecha_baja']
            causa = request.POST['causa']
            historico = int(request.POST['anos_historico'])
            
            # Validar fecha no futura
            if datetime.strptime(fecha_baja, '%Y-%m-%d').date() > timezone.now().date():
                messages.error(request, 'La fecha de baja no puede ser futura')
                return render(request, 'liquidaciones/generar.html', {
                    'empleados': empleados,
                    'min_date': '2000-01-01',
                })
            
            # Validar años históricos razonables
            if historico > 10:
                messages.warning(request, 'El histórico se ha limitado a 10 años')
                historico = 10

            with connection.cursor() as cursor:
                cursor.callproc('sp_generar_liquidacion', [
                    emp_id, fecha_baja, causa, historico
                ])
                # Obtener el resultado del SP si retorna algo
                result = cursor.fetchone()
                if result:
                    messages.success(request, f'Liquidación generada: Q{result[0]:,.2f}')
                else:
                    messages.success(request, 'Liquidación generada correctamente')
            
            return redirect('liquidaciones:listar_liquidaciones')

        except ValueError as e:
            messages.error(request, f'Error en los datos: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error al generar liquidación: {str(e)}')

    return render(request, 'liquidaciones/generar.html', {
        'empleados': empleados,
        'min_date': '2000-01-01',
    })