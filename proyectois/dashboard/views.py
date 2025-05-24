from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages

def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')

#def nomina_view(request):
 #   with connection.cursor() as cursor:
  #      cursor.execute("SELECT id, empleado_id, periodo, monto, fecha_pago FROM nomina")
   #     records = cursor.fetchall()
    #return render(request, 'dashboard/nomina.html', {'nominas': records})

def nomina_view(request):
    # Cargar lista de empleados para el filtro
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_empleados')
        empleados = cursor.fetchall()

    selected_id = request.GET.get('empleado_id', '')
    fecha_pago = request.GET.get('fecha_pago', '')

    # Obtener todas las nóminas
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_nomina')
        nominas = cursor.fetchall()

    # Filtrar por empleado si se seleccionó
    if selected_id:
        nominas = [n for n in nominas if str(n[1]) == selected_id]
    else:
        # Si no hay empleado seleccionado, no mostrar nada
        nominas = []

    # Filtrar por fecha de pago si se proporcionó
    if fecha_pago:
        nominas = [n for n in nominas if n[24].strftime('%Y-%m-%d') == fecha_pago]

    return render(request, 'dashboard/nomina.html', {
        'nominas': nominas,
        'empleados': empleados,
        'selected_id': selected_id
    })

#def nomina_view(request):
 #   with connection.cursor() as cursor:
        # Llamada al procedimiento almacenado
  #      cursor.callproc('sp_listar_nomina')
        # fetchall() devuelve todas las filas del último result set del SP
   #     nominas = cursor.fetchall()
    #return render(request, 'dashboard/nomina.html', {'nominas': nominas})

def recursos_humanos_view(request):
    # Listar empleados vía SP
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_empleados')
        empleados = cursor.fetchall()
    return render(request, 'dashboard/recursos_humanos.html', {
        'empleados': empleados
    })

def alta_empleado(request):
    if request.method == 'POST':
        nombre        = request.POST['nombre']
        apellido      = request.POST['apellido']
        dpi       = request.POST['dpi']
        codigo_empleado       = request.POST['codigo_empleado']
        cargo         = request.POST['cargo']
        salario       = request.POST['salario']
        estado       = request.POST['estado']
        fecha_ingreso = request.POST['fecha_ingreso']
        with connection.cursor() as cursor:
            cursor.callproc('sp_registrar_empleado', [
                nombre, apellido,dpi,codigo_empleado , cargo, salario,estado,fecha_ingreso
            ])
        messages.success(request, 'Empleado registrado correctamente')
        return redirect('recursos_humanos')

    return render(request, 'dashboard/alta_empleado.html')

def baja_empleado(request, emp_id):
    with connection.cursor() as cursor:
        cursor.callproc('sp_eliminar_empleado', [emp_id])
    messages.success(request, 'Empleado eliminado correctamente')
    return redirect('recursos_humanos')

def prestaciones_view(request):
    with connection.cursor() as cursor:
        cursor.execute(" ")
        prestaciones = cursor.fetchall()
    return render(request, 'dashboard/prestaciones.html', {'prestaciones': prestaciones})

def indicadores_view(request):
    with connection.cursor() as cursor:
        cursor.execute(" ")
        indicadores = cursor.fetchall()
    return render(request, 'dashboard/indicadores.html', {'indicadores': indicadores})

def reportes_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, titulo, descripcion, fecha_generacion FROM reportes")
        reportes = cursor.fetchall()
    return render(request, 'dashboard/reportes.html', {'reportes': reportes})

def administrativo_view(request):
    with connection.cursor() as cursor:
        cursor.execute(" ")
        administracion = cursor.fetchall()
    return render(request, 'dashboard/administrativo.html', {'administrativo': administracion})



def registrar_nomina(request):
   # 1) Cargar lista de empleados para el <select> usando SP
    with connection.cursor() as cursor:
        cursor.callproc('sp_listar_empleados')
        empleados = cursor.fetchall()

    context = {'empleados': empleados}

     # 2) Si viene un GET con empleado_id, precargar datos de ese empleado via SP
    emp_id = request.GET.get('empleado_id')
    if emp_id:
        with connection.cursor() as cursor:
            cursor.callproc('sp_obtener_empleado', [emp_id])
            fila = cursor.fetchone()

        if fila:
            context.update({
                'selected_id': emp_id,
                'nombre_completo': f"{fila[0]} {fila[1]}",
                'dpi': fila[2],
                'codigo_empleado': fila[3],
                'cargo': fila[4],
                'salario': fila[5],
            })

    # 3) Al enviar el formulario (POST), invocar el SP autocalculado
    if request.method == 'POST':
        params = [
            request.POST['empleado_id'],
            request.POST['periodo'],
            request.POST['bono_incentivo'],
            request.POST.get('horas_extras', 0),
            request.POST.get('monto_horas_extras', 0),
            request.POST.get('comisiones', 0),
            request.POST.get('viaticos', 0),
            request.POST.get('otros_beneficios', 0),
            request.POST.get('prestamos', 0),
            request.POST.get('otras_deducciones', 0),
            request.POST['fecha_pago'],
        ]
        with connection.cursor() as cursor:
            cursor.callproc('sp_registrar_nomina_autocalc', params)
        messages.success(request, "Nómina registrada con cálculos automáticos")
        return redirect('nomina')

    return render(request, 'dashboard/registrar_nomina.html', context)
