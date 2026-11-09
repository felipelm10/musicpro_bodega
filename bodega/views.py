from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Categoria, Proveedor, Sucursal, Producto, Solicitud, DetalleSolicitud, MovimientoStock
from django.db.models import Count

# ==========================================
# 1. SISTEMA DE AUTENTICACIÓN Y DASHBOARD
# ==========================================
def login_view(request):
    error = None
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Usuario o contraseña incorrectos."
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard.html')


# ==========================================
# 2. CRUD DE PROVEEDORES
# ==========================================
@login_required(login_url='login')
def proveedor_listar(request):
    return render(request, 'proveedor_listar.html', {'proveedores': Proveedor.objects.all()})

@login_required(login_url='login')
def proveedor_crear(request):
    error = None
    if request.method == 'POST':
        rut = request.POST.get('rut', '').strip()
        if Proveedor.objects.filter(rut=rut).exists():
            error = f"Ya existe un proveedor con el RUT {rut}."
        else:
            Proveedor.objects.create(
                rut=rut, razon_social=request.POST.get('razon_social'),
                email=request.POST.get('email'), telefono=request.POST.get('telefono')
            )
            return redirect('proveedores_listar')
    return render(request, 'proveedor_form.html', {'error': error})

@login_required(login_url='login')
def proveedor_editar(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    error = None
    if request.method == 'POST':
        rut = request.POST.get('rut', '').strip()
        if Proveedor.objects.filter(rut=rut).exclude(id=id).exists():
            error = f"Ya existe otro proveedor con el RUT {rut}."
        else:
            proveedor.rut = rut
            proveedor.razon_social = request.POST.get('razon_social')
            proveedor.email = request.POST.get('email')
            proveedor.telefono = request.POST.get('telefono')
            proveedor.save()
            return redirect('proveedores_listar')
    return render(request, 'proveedor_form.html', {'proveedor': proveedor, 'error': error})

@login_required(login_url='login')
def proveedor_eliminar(request, id):
    get_object_or_404(Proveedor, id=id).delete()
    return redirect('proveedores_listar')


# ==========================================
# 3. CRUD DE SUCURSALES
# ==========================================
@login_required(login_url='login')
def sucursal_listar(request):
    return render(request, 'sucursal_listar.html', {'sucursales': Sucursal.objects.all()})

@login_required(login_url='login')
def sucursal_crear(request):
    error = None
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        if Sucursal.objects.filter(codigo=codigo).exists():
            error = f"Ya existe una sucursal con el código {codigo}."
        else:
            Sucursal.objects.create(codigo=codigo, nombre=request.POST.get('nombre'), direccion=request.POST.get('direccion'))
            return redirect('sucursales_listar')
    return render(request, 'sucursal_form.html', {'error': error})

@login_required(login_url='login')
def sucursal_editar(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    error = None
    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip()
        if Sucursal.objects.filter(codigo=codigo).exclude(id=id).exists():
            error = f"Ya existe otra sucursal con el código {codigo}."
        else:
            sucursal.codigo = codigo
            sucursal.nombre = request.POST.get('nombre')
            sucursal.direccion = request.POST.get('direccion')
            sucursal.activa = request.POST.get('activa') == 'on'
            sucursal.save()
            return redirect('sucursales_listar')
    return render(request, 'sucursal_form.html', {'sucursal': sucursal, 'error': error})

@login_required(login_url='login')
def sucursal_eliminar(request, id):
    get_object_or_404(Sucursal, id=id).delete()
    return redirect('sucursales_listar')


# ==========================================
# 4. CRUD DE PRODUCTOS
# ==========================================
@login_required(login_url='login')
def producto_listar(request):
    productos = Producto.objects.select_related('categoria', 'proveedor').all()
    return render(request, 'producto_listar.html', {'productos': productos})

@login_required(login_url='login')
def producto_crear(request):
    error = None
    if not Categoria.objects.exists():
        Categoria.objects.create(nombre="Instrumentos de Cuerda")
        Categoria.objects.create(nombre="Audio Profesional")
        Categoria.objects.create(nombre="Accesorios")

    if request.method == 'POST':
        try:
            Producto.objects.create(
                sku=request.POST.get('sku'), # <--- Capturando el nuevo campo
                nombre=request.POST.get('nombre'),
                precio=request.POST.get('precio'),
                stock_actual=request.POST.get('stock_actual'),
                categoria=get_object_or_404(Categoria, id=request.POST.get('categoria')),
                proveedor=get_object_or_404(Proveedor, id=request.POST.get('proveedor'))
            )
            return redirect('productos_listar')
        except Exception as e:
            error = f"Error devuelto por la base de datos: {e}"

    return render(request, 'producto_form.html', {
        'categorias': Categoria.objects.all(), 'proveedores': Proveedor.objects.all(), 'error': error
    })

@login_required(login_url='login')
def producto_editar(request, id):
    producto = get_object_or_404(Producto, id=id)
    error = None
    if request.method == 'POST':
        try:
            producto.sku = request.POST.get('sku') # <--- Actualizando el nuevo campo
            producto.nombre = request.POST.get('nombre')
            producto.precio = request.POST.get('precio')
            producto.stock_actual = request.POST.get('stock_actual')
            producto.categoria = get_object_or_404(Categoria, id=request.POST.get('categoria'))
            producto.proveedor = get_object_or_404(Proveedor, id=request.POST.get('proveedor'))
            producto.save()
            return redirect('productos_listar')
        except Exception as e:
            error = f"Error devuelto por la base de datos: {e}"

    return render(request, 'producto_form.html', {
        'producto': producto, 'categorias': Categoria.objects.all(), 'proveedores': Proveedor.objects.all(), 'error': error
    })

@login_required(login_url='login')
def producto_eliminar(request, id):
    get_object_or_404(Producto, id=id).delete()
    return redirect('productos_listar')


# ==========================================
# 5. MÓDULO DE REPORTES Y DESPACHO
# ==========================================
@login_required(login_url='login')
def reportes_dashboard(request):
    total_productos = Producto.objects.count()
    productos_criticos = Producto.objects.filter(stock_actual__lte=5).select_related('proveedor')
    productos_por_proveedor = Producto.objects.values('proveedor__razon_social').annotate(total=Count('id')).order_by('-total')

    return render(request, 'reportes.html', {
        'total_productos': total_productos,
        'productos_criticos': productos_criticos,
        'productos_por_proveedor': productos_por_proveedor,
    })

@login_required(login_url='login')
def despachar_producto(request):
    error = None
    mensaje_exito = None

    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        sucursal_id = request.POST.get('sucursal')
        cantidad = int(request.POST.get('cantidad', 0))

        if producto_id and sucursal_id and cantidad > 0:
            producto = get_object_or_404(Producto, id=producto_id)
            
            if cantidad <= producto.stock_actual:
                producto.stock_actual -= cantidad
                producto.save()
                mensaje_exito = f"¡Éxito! Se han despachado {cantidad} unidades de '{producto.nombre}'."
            else:
                error = f"Stock insuficiente. Solo tienes {producto.stock_actual} unidades en bodega."
        else:
            error = "Debes seleccionar un producto, una sucursal y una cantidad válida."

    productos_disponibles = Producto.objects.filter(stock_actual__gt=0)
    sucursales = Sucursal.objects.filter(activa=True)

    return render(request, 'despacho_form.html', {
        'productos': productos_disponibles,
        'sucursales': sucursales,
        'error': error,
        'mensaje_exito': mensaje_exito
    })