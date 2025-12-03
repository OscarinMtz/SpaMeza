from django.db import models
from django.contrib.auth.models import User

class Servicios(models.Model):
    id_servicios = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.IntegerField(help_text="Duración en minutos")
    tipo_servicio = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre
    
    def empleados_asignados(self):
        return ", ".join([emp.nombre_completo() for emp in self.empleados.all()])
    
    def clientes_asignados(self):
        return ", ".join([cli.nombre_completo() for cli in self.clientes.all()])
    
    def productos_utilizados_nombres(self):
        """Mostrar nombres de productos utilizados en este servicio"""
        return ", ".join([prod.nombre for prod in self.productos_utilizados.all()])
    
    def productos_utilizados_detalle(self):
        """Obtener lista detallada de productos utilizados"""
        return self.productos_utilizados.all()
    
    def total_productos_utilizados(self):
        """Cantidad total de productos utilizados"""
        return self.productos_utilizados.count()

class Empleados(models.Model):
    id_empleados = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    cargo = models.CharField(max_length=100)
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, related_name='empleados')
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def servicio_nombre(self):
        return self.servicio.nombre

class Proveedores(models.Model):
    id_proveedores = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=200)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    direccion = models.TextField()
    especialidad = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre_empresa
    
    def productos_proveidos(self):
        return ", ".join([prod.nombre for prod in self.productos.all()])

class Productos(models.Model):
    TIPO_PRODUCTO = [
        ('cosmetico', 'Cosmético'),
        ('equipo', 'Equipo'),
        ('material', 'Material'),
        ('herramienta', 'Herramienta'),
        ('otros', 'Otros'),
    ]
    
    id_productos = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    tipo_producto = models.CharField(max_length=20, choices=TIPO_PRODUCTO)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, related_name='productos')
    servicios = models.ManyToManyField(Servicios, blank=True, related_name='productos_utilizados')
    
    def __str__(self):
        return self.nombre
    
    def nombre_proveedor(self):
        return self.proveedor.nombre_empresa
    
    def servicios_relacionados(self):
        return ", ".join([serv.nombre for serv in self.servicios.all()])
    
    # CORRECCIÓN: Cambiar el método para usar el related_name correcto
    def clientes_interesados_nombres(self):
        return ", ".join([cli.nombre_completo() for cli in self.clientes_interes.all()])

class Clientes(models.Model):
    id_clientes = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cliente')
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateField(auto_now_add=True)
    alergias = models.TextField(blank=True, null=True)
    preferencias = models.TextField(blank=True, null=True)
    
    # Relaciones
    servicios = models.ManyToManyField(Servicios, blank=True, related_name='clientes')
    productos_interes = models.ManyToManyField(Productos, blank=True, related_name='clientes_interes')
    
    def __str__(self):
        if self.usuario:
            return f"{self.nombre} {self.apellido} ({self.usuario.username})"
        return f"{self.nombre} {self.apellido}"
    
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def servicios_contratados(self):
        """Mostrar servicios que realmente ha comprado el cliente"""
        servicios_pedidos = []
        if self.usuario:
            # Buscar en todos los pedidos del usuario
            for pedido in self.usuario.pedidos.all():
                for item in pedido.items.all():
                    if item.servicio and item.servicio not in servicios_pedidos:
                        servicios_pedidos.append(item.servicio)
        
        if servicios_pedidos:
            return ", ".join([serv.nombre for serv in servicios_pedidos])
        return "Sin servicios contratados"
    
    def productos_interes_nombres(self):
        """Mostrar productos que realmente ha comprado el cliente"""
        productos_pedidos = []
        if self.usuario:
            # Buscar en todos los pedidos del usuario
            for pedido in self.usuario.pedidos.all():
                for item in pedido.items.all():
                    if item.producto and item.producto not in productos_pedidos:
                        productos_pedidos.append(item.producto)
        
        if productos_pedidos:
            return ", ".join([prod.nombre for prod in productos_pedidos])
        return "Sin productos comprados"
    
    def pedidos_realizados(self):
        if self.usuario:
            return self.usuario.pedidos.count()
        return 0
    
    def total_gastado(self):
        if self.usuario:
            return sum(pedido.total for pedido in self.usuario.pedidos.all())
        return 0
    
    def ultimo_pedido(self):
        if self.usuario and self.usuario.pedidos.exists():
            return self.usuario.pedidos.latest('fecha_pedido')
        return None

# Modelos de Carrito
class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carritos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    def total_carrito(self):
        return sum(item.subtotal() for item in self.items.all())
    
    def total_items(self):
        return sum(item.cantidad for item in self.items.all())
    
    def tiene_servicios(self):
        return self.items.filter(tipo='servicio').exists()
    
    def tiene_productos(self):
        return self.items.filter(tipo='producto').exists()

class CarritoItem(models.Model):
    TIPO_ITEM = [
        ('producto', 'Producto'),
        ('servicio', 'Servicio'),
    ]
    
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, null=True, blank=True)
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, null=True, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_ITEM, default='producto')
    cantidad = models.IntegerField(default=1)
    
    def __str__(self):
        if self.tipo == 'producto':
            return f"{self.cantidad} x {self.producto.nombre}"
        else:
            return f"{self.cantidad} x {self.servicio.nombre}"
    
    def subtotal(self):
        if self.tipo == 'producto':
            return self.producto.precio * self.cantidad
        else:
            return self.servicio.precio * self.cantidad
    
    def nombre_item(self):
        if self.tipo == 'producto':
            return self.producto.nombre
        else:
            return self.servicio.nombre
    
    def precio_unitario(self):
        if self.tipo == 'producto':
            return self.producto.precio
        else:
            return self.servicio.precio

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('preparando', 'Preparando'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Nuevo
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)      # Nuevo
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Este sería el total con IVA
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    notas = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"
    
    # --- CAMPOS NUEVOS ---
    direccion_entrega = models.TextField(blank=True, null=True)  # Para guardar la dirección
    telefono_contacto = models.CharField(max_length=20, blank=True, null=True) # Para guardar el teléfono

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

    # --- MÉTODOS AYUDANTES NUEVOS (Para usar en "Mis Pedidos") ---
    def tiene_productos(self):
        """Devuelve True si el pedido incluye productos físicos"""
        return self.items.filter(producto__isnull=False).exists()

    def tiene_servicios(self):
        """Devuelve True si el pedido incluye servicios"""
        return self.items.filter(servicio__isnull=False).exists()
    
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, null=True, blank=True)
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    def subtotal(self):
        return self.precio * self.cantidad
    
    def nombre_item(self):
        if self.producto:
            return self.producto.nombre
        elif self.servicio:
            return self.servicio.nombre
        return "Item"