from django.shortcuts import render, redirect
from django.db import connection
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Llamamos al procedimiento almacenado para obtener el usuario y su contraseña hasheada.
        with connection.cursor() as cursor:
            cursor.callproc('sp_obtener_usuario', [username])
            result = cursor.fetchone()
        
        if result:
            user_id, hashed_password = result
            # Comparamos la contraseña ingresada con el hash almacenado.
            if check_password(password, hashed_password):
                request.session['user_id'] = user_id
                return redirect('dashboard')
            else:
                messages.error(request, 'Credenciales inválidas')
        else:
            messages.error(request, 'Credenciales inválidas')
    
    return render(request, 'login.html')


def dashboard(request):
    if not request.session.get('user_id'):
        return redirect('login')
    return render(request, 'dashboard/dashboard.html')

def logout_view(request):
    request.session.flush()  # Limpia la sesión del usuario
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, 'register.html')
        
        # Encriptar la contraseña utilizando el mecanismo de Django.
        encrypted_password = make_password(password)
        
        # Llamar al procedimiento almacenado para registrar el usuario.
        with connection.cursor() as cursor:
            try:
                cursor.callproc('sp_registrar_usuario', [username, encrypted_password, email])
                messages.success(request, "Usuario registrado con éxito. Inicia sesión para continuar.")
                return redirect('login')
            except Exception as e:
                messages.error(request, "Error al registrar usuario: " + str(e))
    
    return render(request, 'register.html')



