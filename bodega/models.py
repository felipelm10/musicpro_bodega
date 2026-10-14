from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, db_index=True)
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    ubicacion = models.CharField(max_length=100)
    precio = models.PositiveIntegerField(default=0)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=5)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('Ingreso', 'Ingreso'),
        ('Salida', 'Salida'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='movimientos')
    cantidad = models.PositiveIntegerField()
    origen_destino = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='movimientos_bodega')

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"

    def __str__(self):
        return f"{self.tipo} ({self.cantidad}) - {self.producto.codigo}"