from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    rut = models.CharField(max_length=20, unique=True)
    razon_social = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.razon_social

class Sucursal(models.Model):
    codigo = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=120)
    direccion = models.CharField(max_length=200)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.sku} - {self.nombre}"

class Solicitud(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('Rechazada', 'Rechazada'),
        ('Despachada', 'Despachada'),
    ]
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=30, choices=ESTADOS, default='Pendiente')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Solicitud {self.id} - {self.sucursal.nombre}"

class DetalleSolicitud(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad_solicitada = models.IntegerField()
    cantidad_aprobada = models.IntegerField(default=0)
    cantidad_despachada = models.IntegerField(default=0)

class MovimientoStock(models.Model):
    TIPO_MOVIMIENTO = [
        ('Entrada', 'Entrada'),
        ('Salida', 'Salida'),
    ]
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    solicitud = models.ForeignKey(Solicitud, on_delete=models.SET_NULL, null=True, blank=True)
    tipo = models.CharField(max_length=15, choices=TIPO_MOVIMIENTO)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    observacion = models.TextField(blank=True, null=True)