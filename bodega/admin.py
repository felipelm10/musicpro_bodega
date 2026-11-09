from django.contrib import admin
from .models import Categoria, Proveedor, Sucursal, Producto, Solicitud, DetalleSolicitud, MovimientoStock

admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(Sucursal)
admin.site.register(Producto)
admin.site.register(Solicitud)
admin.site.register(DetalleSolicitud)
admin.site.register(MovimientoStock)