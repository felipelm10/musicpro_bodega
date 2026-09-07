from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ('Ingreso', 'Ingreso'),
        ('Salida', 'Salida'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    origen_destino = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.tipo} - {self.producto.codigo} ({self.cantidad})"