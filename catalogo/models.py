from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class ProductoQuerySet(models.QuerySet):
    def disponibles(self):
        return self.filter(activo=True, stock__gt=0)

    def buscar(self, termino=''):
        if termino:
            return self.filter(Q(nombre__icontains=termino) | Q(descripcion__icontains=termino))
        return self


class Producto(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    objects = ProductoQuerySet.as_manager()

    class Meta:
        ordering = ['nombre']
        constraints = [models.CheckConstraint(condition=Q(precio__gte=0), name='producto_precio_no_negativo')]

    def __str__(self):
        return self.nombre
