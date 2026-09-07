from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .models import Producto, Movimiento

def jefe_requerido(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def index(request):
    return render(request, 'index.html')

def login_view(request):
    error_mensaje = None
    if request.method == 'POST':
        identificador = request.POST.get('username', '').strip()
        clave_input = request.POST.get('password', '').strip()

        usuario_encontrado = User.objects.filter(
            Q(username__iexact=identificador) | Q(email__iexact=identificador)
        ).first()

        user = None
        if usuario_encontrado:
            user = authenticate(request, username=usuario_encontrado.username, password=clave_input)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('dashboard')
            else:
                error_mensaje = "Esta cuenta ha sido desactivada por el administrador."
        else:
            error_mensaje = "Credenciales incorrectas. Verifique sus datos."

    return render(request, 'login.html', {'error': error_mensaje})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    productos = Producto.objects.all()
    total_productos = productos.count()
    stock_critico = sum(1 for p in productos if p.stock <= p.stock_minimo)
    
    hoy = timezone.now().date()
    movimientos_hoy = Movimiento.objects.filter(fecha__date=hoy).count()

    contexto = {
        'productos': productos,
        'total_productos': total_productos,
        'stock_critico': stock_critico,
        'movimientos_hoy': movimientos_hoy,
    }
    return render(request, 'dashboard.html', contexto)

@login_required(login_url='login')
def historial(request):
    movimientos = Movimiento.objects.select_related('producto', 'responsable').order_by('-fecha')
    return render(request, 'historial.html', {'movimientos': movimientos})

@login_required(login_url='login')
@jefe_requerido
def producto_crear(request):
    if request.method == 'POST':
        Producto.objects.create(
            codigo=request.POST.get('codigo'),
            nombre=request.POST.get('nombre'),
            categoria=request.POST.get('categoria'),
            ubicacion=request.POST.get('ubicacion'),
            stock=int(request.POST.get('stock', 0)),
            stock_minimo=int(request.POST.get('stock_minimo', 3))
        )
        return redirect('dashboard')
    return render(request, 'producto_crear.html')

@login_required(login_url='login')
@jefe_requerido
def producto_editar(request):
    return render(request, 'producto_editar.html')

@login_required(login_url='login')
@jefe_requerido
def ingreso(request):
    error = None
    productos = Producto.objects.all().order_by('nombre')

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 0))
        guia = request.POST.get('guia')
        observaciones = request.POST.get('observaciones')

        producto = get_object_or_404(Producto, id=producto_id)
        if cantidad <= 0:
            error = "La cantidad debe ser mayor a 0."
        else:
            producto.stock += cantidad
            producto.save()

            origen_info = f"Guía/Factura: {guia}" if guia else "Recepción"
            if observaciones:
                origen_info += f" ({observaciones})"

            Movimiento.objects.create(
                tipo='Ingreso',
                producto=producto,
                cantidad=cantidad,
                origen_destino=origen_info,
                responsable=request.user
            )
            return redirect('historial')

    return render(request, 'ingreso.html', {'productos': productos, 'error': error})

@login_required(login_url='login')
@jefe_requerido
def salida(request):
    error = None
    productos = Producto.objects.filter(stock__gt=0)

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = int(request.POST.get('cantidad', 0))
        destino = request.POST.get('destino')
        orden = request.POST.get('orden')

        producto = get_object_or_404(Producto, id=producto_id)
        if cantidad <= 0:
            error = "La cantidad debe ser mayor a 0."
        elif cantidad > producto.stock:
            error = f"Stock insuficiente. Solo quedan {producto.stock} unidades."
        else:
            producto.stock -= cantidad
            producto.save()

            destino_completo = f"{destino} (OT: {orden})" if orden else destino
            Movimiento.objects.create(
                tipo='Salida',
                producto=producto,
                cantidad=cantidad,
                origen_destino=destino_completo,
                responsable=request.user
            )
            return redirect('historial')

    return render(request, 'salida.html', {'productos': productos, 'error': error})

@login_required(login_url='login')
@jefe_requerido
def usuarios_listar(request):
    usuarios = User.objects.all().order_by('id')
    return render(request, 'usuarios_listar.html', {'usuarios': usuarios})

@login_required(login_url='login')
@jefe_requerido
def usuario_crear(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if User.objects.filter(username=username).exists():
            error = f"El usuario/RUT '{username}' ya existe."
        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=nombre,
                is_staff=(rol == 'jefe')
            )
            return redirect('usuarios_listar')

    return render(request, 'usuario_crear.html', {'error': error})

@login_required(login_url='login')
@jefe_requerido
def usuario_editar(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        usuario.first_name = request.POST.get('nombre')
        usuario.email = request.POST.get('email')
        usuario.is_staff = (request.POST.get('rol') == 'jefe')
        usuario.is_active = ('activo' in request.POST)
        nueva_clave = request.POST.get('password')
        if nueva_clave:
            usuario.set_password(nueva_clave)
        usuario.save()
        return redirect('usuarios_listar')

    return render(request, 'usuario_editar.html', {'usr': usuario})