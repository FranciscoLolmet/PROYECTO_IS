from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('registrar_nomina/', views.registrar_nomina, name='registrar_nomina'),
    path('alta_empleado/', views.alta_empleado,    name='alta_empleado'),
    path('recursos-humanos/baja/<int:emp_id>/', views.baja_empleado, name='baja_empleado'),
    path('nomina/', views.nomina_view, name='nomina'),
    path('recursos-humanos/', views.recursos_humanos_view, name='recursos_humanos'),
    path('prestaciones/', views.prestaciones_view, name='prestaciones'),
    path('indicadores/', views.indicadores_view, name='indicadores'),
    path('reportes/', views.reportes_view, name='reportes'),
    path('administrativo/', views.administrativo_view, name='administrativo'),
    path('dashboard/liquidaciones/', include('liquidaciones.urls')),
    path('dashboard/roles/', include('roles.urls')),
    path('dashboard/vacaciones/', include('vacaciones.urls')),
]
