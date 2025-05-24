from django.urls import path
from . import views

app_name = 'liquidaciones'
urlpatterns = [
    path('', views.listar_liquidaciones, name='listar_liquidaciones'),
    path('generar/', views.generar_liquidacion, name='generar_liquidacion'),
]