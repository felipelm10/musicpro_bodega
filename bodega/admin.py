from django.contrib import admin
from .models import Categoria, Producto, Movimiento

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'categoria', 'stock', 'stock_minimo', 'precio', 'ubicacion')
    list_filter = ('categoria', 'ubicacion')
    search_fields = ('codigo', 'nombre')
    list_editable = ('stock', 'precio')
    list_per_page = 25


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo', 'producto', 'cantidad', 'origen_destino', 'responsable', 'fecha')
    list_filter = ('tipo', 'fecha')
    search_fields = ('producto__nombre', 'producto__codigo', 'origen_destino')
    readonly_fields = ('fecha',)
    list_per_page = 25