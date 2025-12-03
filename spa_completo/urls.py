from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app_spa import views as spa_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', spa_views.inicio, name='inicio'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', spa_views.custom_logout, name='logout'),
    path('registro/', spa_views.registro, name='registro'),
    path('tienda/', spa_views.tienda, name='tienda'),
    path('carrito/', spa_views.carrito, name='carrito'),
    path('agregar-carrito/<int:producto_id>/', spa_views.agregar_carrito, name='agregar_carrito'),
    path('agregar-servicio-carrito/<int:servicio_id>/', spa_views.agregar_servicio_carrito, name='agregar_servicio_carrito'),
    path('eliminar-carrito/<int:item_id>/', spa_views.eliminar_carrito, name='eliminar_carrito'),
    path('actualizar-carrito/<int:item_id>/', spa_views.actualizar_carrito, name='actualizar_carrito'),
    path('checkout/', spa_views.checkout, name='checkout'),
    path('pedidos/', spa_views.mis_pedidos, name='mis_pedidos'),
    path('cancelar-pedido/<int:pedido_id>/', spa_views.cancelar_pedido, name='cancelar_pedido'),
    path('eliminar-pedido/<int:pedido_id>/', spa_views.eliminar_pedido, name='eliminar_pedido'),
    
    # URLs de administración (SOLO PARA STAFF/ADMIN)
    path('admin-spa/servicios/', spa_views.servicios_lista, name='servicios_lista'),
    path('admin-spa/servicios/agregar/', spa_views.servicio_agregar, name='servicio_agregar'),
    path('admin-spa/servicios/editar/<int:id>/', spa_views.servicio_editar, name='servicio_editar'),
    path('admin-spa/servicios/eliminar/<int:id>/', spa_views.servicio_eliminar, name='servicio_eliminar'),
    
    path('admin-spa/empleados/', spa_views.empleados_lista, name='empleados_lista'),
    path('admin-spa/empleados/agregar/', spa_views.empleado_agregar, name='empleado_agregar'),
    path('admin-spa/empleados/editar/<int:id>/', spa_views.empleado_editar, name='empleado_editar'),
    path('admin-spa/empleados/eliminar/<int:id>/', spa_views.empleado_eliminar, name='empleado_eliminar'),
    
    path('admin-spa/clientes/', spa_views.clientes_lista, name='clientes_lista'),
    path('admin-spa/clientes/agregar/', spa_views.cliente_agregar, name='cliente_agregar'),
    path('admin-spa/clientes/editar/<int:id>/', spa_views.cliente_editar, name='cliente_editar'),
    path('admin-spa/clientes/eliminar/<int:id>/', spa_views.cliente_eliminar, name='cliente_eliminar'),
    
    path('admin-spa/proveedores/', spa_views.proveedores_lista, name='proveedores_lista'),
    path('admin-spa/proveedores/agregar/', spa_views.proveedor_agregar, name='proveedor_agregar'),
    path('admin-spa/proveedores/editar/<int:id>/', spa_views.proveedor_editar, name='proveedor_editar'),
    path('admin-spa/proveedores/eliminar/<int:id>/', spa_views.proveedor_eliminar, name='proveedor_eliminar'),
    
    path('admin-spa/productos/', spa_views.productos_lista, name='productos_lista'),
    path('admin-spa/productos/agregar/', spa_views.producto_agregar, name='producto_agregar'),
    path('admin-spa/productos/editar/<int:id>/', spa_views.producto_editar, name='producto_editar'),
    path('admin-spa/productos/eliminar/<int:id>/', spa_views.producto_eliminar, name='producto_eliminar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)