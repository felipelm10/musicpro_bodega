import time
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from bodega.models import Categoria, Producto

class Command(BaseCommand):
    help = 'Genera registros masivos de prueba para la bodega con Faker'

    def add_arguments(self, parser):
        # Permite recibir el número deseado desde la terminal (ej: 100, 1000)
        parser.add_argument('cantidad', type=int, help='Cantidad de productos a generar')

    def handle(self, *args, **kwargs):
        cantidad = kwargs['cantidad']
        fake = Faker('es_CL')  # Genera datos contextualizados en español

        self.stdout.write(self.style.WARNING(f"Iniciando la creación de {cantidad:,} registros..."))
        tiempo_inicio = time.time()

        # 1. Asegurar categorías base para asociar los productos (claves foráneas)
        nombres_cat = ['Cuerdas', 'Percusión', 'Teclados', 'Viento', 'Audio Pro', 'Accesorios']
        categorias = [Categoria.objects.get_or_create(nombre=c)[0] for c in nombres_cat]

        lote = []
        tamano_lote = 5000  # Inserta de a 5.000 filas para no saturar la memoria RAM
        total_insertados = 0

        # 2. Transacción atómica: acelera la escritura en SQLite hasta 100 veces
        with transaction.atomic():
            for i in range(1, cantidad + 1):
                cat_seleccionada = categorias[i % len(categorias)]

                # Faker inventa los valores aquí:
                lote.append(
                    Producto(
                        codigo=f"PROD-{fake.bothify(text='??-########')}",
                        nombre=f"{fake.word().capitalize()} {fake.color_name().capitalize()}",
                        categoria=cat_seleccionada,
                        ubicacion=f"Pasillo {fake.random_element(('A', 'B', 'C', 'D'))}-Rack {fake.random_int(1, 10)}",
                        precio=fake.random_int(min=5000, max=1200000, step=1000),
                        stock=fake.random_int(min=0, max=150),
                        stock_minimo=fake.random_int(min=2, max=8),
                    )
                )

                # Cuando el lote llega a 5.000, se guarda en bloque en la base de datos
                if len(lote) >= tamano_lote:
                    Producto.objects.bulk_create(lote)
                    total_insertados += len(lote)
                    self.stdout.write(f"Guardados: {total_insertados:,} / {cantidad:,}")
                    lote = []

            # Guardar el residuo final que haya quedado en memoria
            if lote:
                Producto.objects.bulk_create(lote)
                total_insertados += len(lote)

        tiempo_total = time.time() - tiempo_inicio
        self.stdout.write(self.style.SUCCESS(
            f"Listo: Se generaron e insertaron {total_insertados:,} registros en {tiempo_total:.2f} segundos."
        ))