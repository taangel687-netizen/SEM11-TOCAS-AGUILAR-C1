from decimal import Decimal
from io import StringIO
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import TestCase
from django.urls import resolve, reverse
from .models import Producto
from .views import ProductoListView


class CatalogoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.producto = Producto.objects.create(nombre="laptop", precio=Decimal("100.50"), stock=2)
        Producto.objects.create(nombre="agotado", precio=10, stock=0)
        Producto.objects.create(nombre="inactivo", precio=20, stock=5, activo=False)

    def test_home_contexto_y_herencia(self):
        respuesta = self.client.get(reverse("catalogo:home"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["total"], 3)
        self.assertEqual(respuesta.context["disponibles"], 1)
        self.assertTemplateUsed(respuesta, "catalogo/base.html")

    def test_ruta_cbv_y_filtro_title(self):
        ruta = reverse("catalogo:lista")
        self.assertIs(resolve(ruta).func.view_class, ProductoListView)
        self.assertContains(self.client.get(ruta), "Laptop")

    def test_busqueda_y_disponibilidad(self):
        respuesta = self.client.get(reverse("catalogo:lista"), {"q": "LAP", "disponibles": "1"})
        self.assertQuerySetEqual(respuesta.context["productos"], [self.producto])
        self.assertEqual(Producto.objects.disponibles().count(), 1)

    def test_estado_vacio_y_escape_html(self):
        respuesta = self.client.get(reverse("catalogo:lista"), {"q": "<script>alert(1)</script>"})
        self.assertContains(respuesta, "No encontramos productos")
        self.assertNotContains(respuesta, "<script>alert(1)</script>")

    def test_paginacion_y_parametros(self):
        for i in range(8):
            Producto.objects.create(nombre=f"equipo {i}", precio=5, stock=1)
        respuesta = self.client.get(reverse("catalogo:lista"), {"q": "equipo", "disponibles": "1"})
        self.assertEqual(len(respuesta.context["productos"]), 6)
        self.assertContains(respuesta, "q=equipo")
        self.assertContains(respuesta, "disponibles=1")
        segunda = self.client.get(reverse("catalogo:lista"), {"q": "equipo", "page": 2})
        self.assertEqual(len(segunda.context["productos"]), 2)
        self.assertEqual(self.client.get(reverse("catalogo:lista"), {"page": 999}).status_code, 404)

    def test_modelo_y_validacion(self):
        self.assertEqual(str(self.producto), "laptop")
        self.producto.precio = -1
        with self.assertRaises(ValidationError):
            self.producto.full_clean()

    def test_carga_repetible_sin_duplicados(self):
        call_command("poblar_productos", stdout=StringIO())
        cantidad = Producto.objects.count()
        call_command("poblar_productos", stdout=StringIO())
        self.assertEqual(Producto.objects.count(), cantidad)

    def test_admin_requiere_autenticacion(self):
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 302)
