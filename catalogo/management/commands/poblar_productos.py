from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from catalogo.models import Producto

DATOS = [
    ('laptop para desarrollo', '16 GB RAM y SSD de 512 GB para tus proyectos.', '2899.00', 8, True),
    ('teclado mecánico', 'Teclas precisas y conexión USB para programar.', '189.90', 15, True),
    ('mouse inalámbrico', 'Diseño ergonómico y sensor de alta precisión.', '79.50', 20, True),
    ('monitor de 24 pulgadas', 'Panel Full HD para ampliar tu espacio de trabajo.', '649.00', 5, True),
    ('hub usb c', 'Conecta tus periféricos desde un solo puerto.', '129.00', 0, True),
    ('audífonos de estudio', 'Audio claro para tus clases y reuniones.', '159.90', 12, True),
    ('base para laptop', 'Soporte ajustable de aluminio.', '89.00', 6, True),
    ('webcam full hd', 'Cámara para videollamadas y presentaciones.', '139.00', 3, False),
]

class Command(BaseCommand):
    help = 'Carga productos de demostración sin duplicarlos ni modificar los existentes.'

    @transaction.atomic
    def handle(self, *args, **options):
        creados = 0
        for nombre, descripcion, precio, stock, activo in DATOS:
            _, nuevo = Producto.objects.get_or_create(nombre=nombre, defaults={
                'descripcion': descripcion, 'precio': Decimal(precio), 'stock': stock, 'activo': activo})
            creados += nuevo
        self.stdout.write(self.style.SUCCESS(f'{creados} creados; {Producto.objects.count()} productos en total.'))
