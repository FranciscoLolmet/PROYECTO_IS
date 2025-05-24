from django.urls import path
from . import views

app_name = 'vacaciones'
urlpatterns = [
    path('', views.listar_vacaciones, name='listar_vacaciones'),
    path('registrar/', views.registrar_vacacion, name='registrar_vacacion'),
]