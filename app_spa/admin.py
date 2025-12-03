from django.contrib import admin
from .models import Servicios, Empleados, Proveedores, Productos, Clientes, Carrito, CarritoItem, Pedido, PedidoItem

@admin.register(Servicios)
class ServiciosAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'duracion', 'tipo_servicio', 'empleados_asignados', 'clientes_asignados', 'productos_utilizados_nombres']
    search_fields = ['nombre', 'tipo_servicio']
    list_filter = ['tipo_servicio']

@admin.register(Empleados)
class EmpleadosAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'especialidad', 'cargo', 'servicio_nombre', 'telefono']
    list_filter = ['cargo', 'servicio']
    search_fields = ['nombre', 'apellido']

@admin.register(Proveedores)
class ProveedoresAdmin(admin.ModelAdmin):
    list_display = ['nombre_empresa', 'contacto', 'telefono', 'email', 'especialidad', 'productos_proveidos']
    search_fields = ['nombre_empresa', 'contacto']

@admin.register(Productos)
class ProductosAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'tipo_producto', 'nombre_proveedor', 'servicios_relacionados', 'clientes_interesados_nombres', 'estado_stock']
    list_filter = ['tipo_producto', 'proveedor']
    search_fields = ['nombre', 'descripcion']
    filter_horizontal = ['servicios']
    
    def estado_stock(self, obj):
        if obj.stock > 10:
            return 'Alto'
        elif obj.stock > 0:
            return 'Medio'
        else:
            return 'Agotado'
    estado_stock.short_description = 'Estado Stock'

@admin.register(Clientes)
class ClientesAdmin(admin.ModelAdmin):
    list_display = [
        'nombre_completo', 
        'usuario', 
        'email', 
        'telefono', 
        'fecha_registro', 
        'pedidos_realizados', 
        'total_gastado',
        'servicios_contratados', 
        'productos_interes_nombres',
        'activo'
    ]
    list_filter = ['fecha_registro', 'servicios']
    search_fields = ['nombre', 'apellido', 'email', 'usuario__username']
    readonly_fields = [
        'pedidos_realizados', 
        'total_gastado', 
        'usuario_info',
        'servicios_contratados_detalle',
        'productos_interes_detalle',
        'historial_pedidos'
    ]
    list_editable = ['telefono']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('usuario', 'nombre', 'apellido', 'email', 'telefono')
        }),
        ('Información del Sistema', {
            'fields': ('usuario_info', 'pedidos_realizados', 'total_gastado', 'fecha_registro')
        }),
        ('Servicios y Productos', {
            'fields': ('servicios', 'productos_interes')
        }),
        ('Historial Real', {
            'fields': ('servicios_contratados_detalle', 'productos_interes_detalle', 'historial_pedidos')
        }),
    )
    
    def usuario_info(self, obj):
        if obj.usuario:
            status = "🟢 Activo" if obj.usuario.is_active else "🔴 Inactivo"
            return f"Username: {obj.usuario.username} - Status: {status} - Último login: {obj.usuario.last_login}"
        return "No asociado a usuario"
    usuario_info.short_description = 'Información de Usuario'
    
    def servicios_contratados_detalle(self, obj):
        """Mostrar servicios que realmente ha comprado"""
        servicios = []
        if obj.usuario:
            for pedido in obj.usuario.pedidos.all():
                for item in pedido.items.all():
                    if item.servicio and item.servicio not in servicios:
                        servicios.append(item.servicio)
        
        if servicios:
            html = "<ul>"
            for servicio in servicios:
                html += f"<li>{servicio.nombre} - ${servicio.precio}</li>"
            html += "</ul>"
            return html
        return "No ha contratado servicios aún"
    servicios_contratados_detalle.short_description = 'Servicios Contratados (Real)'
    servicios_contratados_detalle.allow_tags = True
    
    def productos_interes_detalle(self, obj):
        """Mostrar productos que realmente ha comprado"""
        productos = []
        if obj.usuario:
            for pedido in obj.usuario.pedidos.all():
                for item in pedido.items.all():
                    if item.producto and item.producto not in productos:
                        productos.append(item.producto)
        
        if productos:
            html = "<ul>"
            for producto in productos:
                html += f"<li>{producto.nombre} - ${producto.precio} (Stock: {producto.stock})</li>"
            html += "</ul>"
            return html
        return "No ha comprado productos aún"
    productos_interes_detalle.short_description = 'Productos Comprados (Real)'
    productos_interes_detalle.allow_tags = True
    
    def historial_pedidos(self, obj):
        """Mostrar historial completo de pedidos"""
        if obj.usuario and obj.usuario.pedidos.exists():
            html = "<table width='100%' style='border-collapse: collapse;'>"
            html += "<tr style='background-color: #f8f9fa;'><th>Pedido ID</th><th>Fecha</th><th>Total</th><th>Estado</th><th>Items</th></tr>"
            for pedido in obj.usuario.pedidos.all().order_by('-fecha_pedido'):
                items = []
                for item in pedido.items.all():
                    if item.producto:
                        items.append(f"{item.cantidad}x {item.producto.nombre}")
                    elif item.servicio:
                        items.append(f"{item.cantidad}x {item.servicio.nombre}")
                
                estado_color = {
                    'pendiente': '🟡',
                    'confirmado': '🔵', 
                    'completado': '🟢',
                    'cancelado': '🔴'
                }.get(pedido.estado, '⚪')
                
                html += f"""
                <tr style='border-bottom: 1px solid #dee2e6;'>
                    <td>#{pedido.id}</td>
                    <td>{pedido.fecha_pedido.date()}</td>
                    <td>${pedido.total}</td>
                    <td>{estado_color} {pedido.get_estado_display()}</td>
                    <td>{", ".join(items) if items else "Sin items"}</td>
                </tr>
                """
            html += "</table>"
            return html
        return "No tiene historial de pedidos"
    historial_pedidos.short_description = 'Historial Completo de Pedidos'
    historial_pedidos.allow_tags = True
    
    def activo(self, obj):
        return obj.usuario.is_active if obj.usuario else False
    activo.boolean = True
    activo.short_description = 'Activo'
@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'fecha_creacion', 'activo', 'total_items', 'total_carrito']

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ['carrito', 'nombre_item', 'tipo', 'cantidad', 'subtotal']
    list_filter = ['tipo', 'carrito']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'cliente_asociado', 'fecha_pedido', 'total', 'estado', 'items_detallados']
    list_filter = ['estado', 'fecha_pedido']
    readonly_fields = ['cliente_info', 'items_detalle']
    search_fields = ['usuario__username', 'usuario__email', 'id']
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('usuario', 'cliente_info', 'fecha_pedido', 'total', 'estado')
        }),
        ('Items del Pedido', {
            'fields': ('items_detalle',)
        }),
    )
    
    def cliente_asociado(self, obj):
        cliente = obj.cliente_asociado()
        if cliente:
            return f"{cliente.nombre_completo}"
        return "No asociado"
    cliente_asociado.short_description = 'Cliente'
    
    def cliente_info(self, obj):
        cliente = obj.cliente_asociado()
        if cliente:
            return f"""
            <strong>Cliente:</strong> {cliente.nombre_completo}<br>
            <strong>Email:</strong> {cliente.email}<br>
            <strong>Teléfono:</strong> {cliente.telefono}<br>
            <strong>Alergias:</strong> {cliente.alergias or 'Ninguna'}<br>
            <strong>Preferencias:</strong> {cliente.preferencias or 'Ninguna'}
            """
        return "No hay información del cliente disponible"
    cliente_info.short_description = 'Información del Cliente'
    cliente_info.allow_tags = True
    
    def items_detallados(self, obj):
        return obj.items_detallados()
    items_detallados.short_description = 'Items del Pedido'
    
    def items_detalle(self, obj):
        items_html = "<table width='100%'><tr><th>Item</th><th>Tipo</th><th>Cantidad</th><th>Precio</th><th>Subtotal</th></tr>"
        for item in obj.items.all():
            if item.producto:
                items_html += f"<tr><td>{item.producto.nombre}</td><td>Producto</td><td>{item.cantidad}</td><td>${item.precio}</td><td>${item.subtotal()}</td></tr>"
            elif item.servicio:
                items_html += f"<tr><td>{item.servicio.nombre}</td><td>Servicio</td><td>{item.cantidad}</td><td>${item.precio}</td><td>${item.subtotal()}</td></tr>"
        items_html += f"<tr style='background-color: #f8f9fa;'><td colspan='4'><strong>Total</strong></td><td><strong>${obj.total}</strong></td></tr>"
        items_html += "</table>"
        return items_html
    items_detalle.short_description = 'Detalle de Items'
    items_detalle.allow_tags = True

@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'nombre_item', 'cantidad', 'precio', 'subtotal']
    list_filter = ['pedido']