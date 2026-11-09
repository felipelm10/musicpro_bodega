from django.urls import path
from . import views

urlpatterns = [
    # Dashboard y Autenticación
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # CRUD Proveedores
    path('proveedores/', views.proveedor_listar, name='proveedores_listar'),
    path('proveedores/nuevo/', views.proveedor_crear, name='proveedor_crear'),
    path('proveedores/editar/<int:id>/', views.proveedor_editar, name='proveedor_editar'),
    path('proveedores/eliminar/<int:id>/', views.proveedor_eliminar, name='proveedor_eliminar'),

    # CRUD Sucursales
    path('sucursales/', views.sucursal_listar, name='sucursales_listar'),
    path('sucursales/nueva/', views.sucursal_crear, name='sucursal_crear'),
    path('sucursales/editar/<int:id>/', views.sucursal_editar, name='sucursal_editar'),
    path('sucursales/eliminar/<int:id>/', views.sucursal_eliminar, name='sucursal_eliminar'),

    # CRUD Productos
    path('productos/', views.producto_listar, name='productos_listar'),
    path('productos/nuevo/', views.producto_crear, name='producto_crear'),
    path('productos/editar/<int:id>/', views.producto_editar, name='producto_editar'),
    path('productos/eliminar/<int:id>/', views.producto_eliminar, name='producto_eliminar'),

    # Módulo de Reportes
    path('reportes/', views.reportes_dashboard, name='reportes'),
    
    # Módulo Logístico (La guinda de la torta)
    path('despachar/', views.despachar_producto, name='despachar'),
]