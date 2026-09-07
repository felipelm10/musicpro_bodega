from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('productos/nuevo/', views.producto_crear, name='producto_crear'),
    path('productos/editar/', views.producto_editar, name='producto_editar'),
    path('movimientos/ingreso/', views.ingreso, name='ingreso'),
    path('movimientos/salida/', views.salida, name='salida'),
    path('movimientos/historial/', views.historial, name='historial'),
    path('usuarios/', views.usuarios_listar, name='usuarios_listar'),
    path('usuarios/nuevo/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/editar/<int:user_id>/', views.usuario_editar, name='usuario_editar'),
]