from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from .models import Producto


def home(request):
    return render(request, 'catalogo/home.html', {
        'total': Producto.objects.count(),
        'disponibles': Producto.objects.disponibles().count(),
        'fecha': timezone.localdate(),
    })


class ProductoListView(ListView):
    model = Producto
    template_name = 'catalogo/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 6

    def get_queryset(self):
        productos = Producto.objects.all().buscar(self.request.GET.get('q', '').strip())
        if self.request.GET.get('disponibles') == '1':
            productos = productos.disponibles()
        return productos

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto.update(q=self.request.GET.get('q', '').strip(),
                        solo_disponibles=self.request.GET.get('disponibles') == '1',
                        fecha=timezone.localdate())
        return contexto
