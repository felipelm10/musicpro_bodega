import os
import django
from faker import Faker
import random

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicpro_core.settings')
django.setup()

from bodega.models import Categoria, Proveedor, Sucursal, Producto

def poblar_datos():
    fake = Faker('es_CL') # Usamos Faker en español de Chile
    
    print("🧹 Limpiando datos antiguos...")
    Producto.objects.all().delete()
    Proveedor.objects.all().delete()
    Sucursal.objects.all().delete()
    Categoria.objects.all().delete()

    print("📦 Creando Categorías...")
    cat_nombres = ["Guitarras", "Bajos", "Baterías", "Pianos", "Audio Profesional"]
    categorias = [Categoria.objects.create(nombre=n) for n in cat_nombres]

    print("🏭 Creando Proveedores con Faker...")
    proveedores = []
    for _ in range(5):
        prov = Proveedor.objects.create(
            rut=fake.rut(),
            razon_social=fake.company(),
            email=fake.company_email(),
            telefono=fake.phone_number()
        )
        proveedores.append(prov)

    print("🏢 Creando Sucursales con Faker...")
    sucursales = []
    for i in range(4):
        suc = Sucursal.objects.create(
            codigo=f"SUC-{i+100}",
            nombre=f"Sucursal {fake.city()}",
            direccion=fake.street_address(),
            activa=True
        )
        sucursales.append(suc)

    print("🎸 Creando Productos con Faker...")
    for _ in range(15):
        Producto.objects.create(
            sku=fake.unique.bothify(text='PROD-####'),
            nombre=fake.catch_phrase(),
            precio=random.randint(50000, 1500000),
            stock_actual=random.randint(2, 50),
            categoria=random.choice(categorias),
            proveedor=random.choice(proveedores)
        )
        
    print("✅ ¡Base de datos poblada exitosamente con Faker!")

if __name__ == '__main__':
    poblar_datos()