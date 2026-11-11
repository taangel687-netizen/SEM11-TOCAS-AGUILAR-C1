# Semana 11 — Introducción a Django

**Estudiante:** Tocas Anglas Angel
**Docente:** AGUILAR CORONACIÓN MIGUEL ELIAS
**Asignatura:** Desarrollo de Aplicaciones Web (IS093A), IX semestre, UNCP
**Fecha:** 11 de noviembre de 2026

Campus Tech es un catálogo académico desarrollado para la Guía Práctica de la Semana 11. Implementa Django 5.2, arquitectura MTV, enrutamiento reversible, vistas FBV y CBV, herencia de plantillas y persistencia SQLite mediante ORM.

## Ejecutar en Windows PowerShell

Requiere Python 3.11 o posterior. Verificado con Python 3.14 y Django 5.2.19.

```powershell
git clone https://github.com/taangel687-netizen/SEM11-TOCAS-AGUILAR-C1.git
cd SEM11-TOCAS-AGUILAR-C1
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py poblar_productos
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

Abre http://127.0.0.1:8000/ y usa el enlace Catálogo. No es necesario activar el entorno, por lo que no hace falta cambiar la política de ejecución de PowerShell.

`poblar_productos` crea 8 productos sin duplicar ni sobrescribir los existentes. Incluye 6 disponibles, 1 agotado y 1 inactivo. La base SQLite se genera localmente y se excluye de Git.

## Los cinco pasos de la guía

1. **Entorno y estructura:** `python -m venv .venv`, instalación de Django, `python -m django startproject config .` y `python manage.py startapp catalogo`. La aplicación está registrada en `INSTALLED_APPS`.
2. **Rutas:** `config/urls.py` incluye `catalogo.urls`. Los nombres `catalogo:home` y `catalogo:lista` se usan con `{% url %}`. Las plantillas no fijan las rutas a mano.
3. **Vistas:** `home` es una FBV con `render()` y contexto; `ProductoListView` hereda de `ListView`, filtra con `get_queryset()` y amplía el contexto con `get_context_data()`. Las consultas reutilizables están en `ProductoQuerySet`.
4. **Plantillas:** `base.html` define bloques; `home.html` y `catalogo.html` heredan con `extends`. Se usan `for`, `empty`, `if`, `title`, `date`, `floatformat` y `urlencode`. El CSS propio se carga mediante `static`.
5. **Modelo y ORM:** `Producto` define nombre, descripción, precio decimal, stock, activo y fecha. Incluye `__str__`, validación y restricción de precio no negativo. La migración inicial está versionada.

## Consultas ORM

```powershell
.\.venv\Scripts\python.exe manage.py shell
```

```python
from catalogo.models import Producto
productos = Producto.objects.all()  # QuerySet aún no evaluado
list(productos)                     # Ejecuta la consulta
Producto.objects.filter(activo=True, stock__gt=0)
Producto.objects.disponibles().buscar("laptop")
```

Un QuerySet se evalúa al iterarlo, convertirlo en lista o realizar operaciones que necesitan sus resultados. El ORM mantiene las consultas fuera de las plantillas.

## Verificación

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.\.venv\Scripts\python.exe manage.py test
```

8 pruebas cubren inicio, contexto y herencia, ruta CBV, búsqueda, disponibilidad, estado vacío, escape HTML, paginación, validación del modelo, carga repetible y acceso al admin. La revisión del navegador comprobó paginación y ausencia de desborde horizontal a 390 px.

## Estructura

```text
config/                        Configuración y URLs principales
catalogo/models.py             Modelo y QuerySet
catalogo/views.py              FBV y ListView
catalogo/urls.py               Rutas con namespace
catalogo/templates/catalogo/   Base, inicio y catálogo
catalogo/static/catalogo/      Hoja de estilos
catalogo/migrations/           Esquema reproducible
catalogo/management/commands/  Carga de demostración
catalogo/tests.py              Pruebas funcionales
informe/                       Informe y evidencias
requirements.txt              Dependencias fijadas
```

## Preparación para la semana 12

Admin, autenticación, sesiones y middleware CSRF conservan la configuración base de Django. Producto está registrado en admin. Para usarlo ejecuta `python manage.py createsuperuser` con el intérprete del entorno y abre `/admin/`. No hay usuarios ni contraseñas precargados. Los formularios de edición y el flujo de sesiones quedan para la siguiente semana.

Este proyecto es para laboratorio: `DEBUG=True`, clave de desarrollo y servidor local. Para un despliegue se requiere configurar una clave privada mediante `DJANGO_SECRET_KEY`, desactivar DEBUG y configurar hosts y HTTPS. La fuente tipográfica externa es opcional; existen fuentes locales de respaldo.

## Informe y evidencias

El informe DOCX en `informe/` detalla el desarrollo en los cinco pasos. Las imágenes de la aplicación son capturas del navegador; las imágenes de código y comandos son capturas de registros de ejecución local presentados en HTML para facilitar su lectura. Los registros `.txt` permiten verificar la salida sin depender de una imagen.

## Referencias

- https://docs.djangoproject.com/en/5.2/intro/tutorial01/
- https://docs.djangoproject.com/en/5.2/topics/class-based-views/generic-display/
- https://docs.djangoproject.com/en/5.2/topics/templates/
- https://docs.djangoproject.com/en/5.2/topics/db/queries/
