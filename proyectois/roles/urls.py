from django.urls import path
from . import views

app_name = 'roles'
urlpatterns = [
    path('', views.listar_roles, name='listar_roles'),
    path('crear/', views.crear_rol,   name='crear_rol'),
    path('asignar/', views.asignar_rol, name='asignar_rol'),
]