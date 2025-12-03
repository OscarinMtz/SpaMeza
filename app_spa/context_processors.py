from .models import Carrito

def carrito_counter(request):
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user, activo=True)
            return {'carrito_count': carrito.total_items()}
        except Carrito.DoesNotExist:
            return {'carrito_count': 0}
    return {'carrito_count': 0}