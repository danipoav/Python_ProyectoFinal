from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from . import db, bcrypt
from .models import Usuario,Producto,Proveedor,Venta
from .forms import RegistroForm, LoginForm, ProductoForm, ProveedorForm
from collections import defaultdict
from flask import Blueprint
from . import login_manager
from .models import Usuario
from datetime import datetime,timezone
from flask import session


main = Blueprint('main', __name__)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@main.route('/')
def home():
    if current_user.is_authenticated:
        if current_user.rol == 'admin':
            return render_template('home.html')
        else:
            ventas = Venta.query.filter_by(usuario_id = current_user.id).order_by(Venta.fecha.desc()).limit(3).all()
            print(ventas)
            return render_template('cliente/homeCliente.html',ventas = ventas)
    return render_template('bienvenida.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistroForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            password=hashed_pw,
            rol=form.rol.data
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('✅ Cuenta creada correctamente. ¡Ya puedes iniciar sesión!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            flash(f'👋 Bienvenido, {usuario.nombre}', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('❌ Error en email o contraseña', 'danger')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('🔒 Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('main.login'))


#Catalogo de productos
@main.route('/catalogo')
@login_required
def catalogo():
    if current_user.rol != 'cliente':
        flash('Acceso solo para clientes')
        return redirect(url_for('main.home'))
    
    productos = Producto.query.all()
    return render_template('cliente/catalogo.html',productos=productos)

# Productos
@main.route('/productos')
@login_required
def listar_productos():
    productos = Producto.query.all()
    productos_stock_bajo = [
        p for p in productos if p.cantidad <= (p.stock_maximo * 0.1)
    ]
    return render_template('productos/listar.html', productos=productos, productos_stock_bajo=productos_stock_bajo)


@main.route('/producto/nuevo', methods=['GET', 'POST'])
@login_required
def crear_producto():
    form = ProductoForm()
    form.proveedores.choices = [(p.id, p.nombre_empresa) for p in Proveedor.query.all()]

    if form.validate_on_submit():
        nuevo_producto = Producto(
            nombre=form.nombre.data,
            descripcion=form.descripcion.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data,
            ubicacion=form.ubicacion.data,
            referencia=form.referencia.data,
            color=form.color.data
        )
        for prov_id in form.proveedores.data:
            proveedor = Proveedor.query.get(prov_id)
            nuevo_producto.proveedores.append(proveedor)

        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto creado correctamente.', 'success')
        return redirect(url_for('main.listar_productos'))
    
    return render_template('productos/formulario.html', form=form, titulo='Nuevo Producto')

@main.route('/producto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)
    form.proveedores.choices = [(p.id, p.nombre_empresa) for p in Proveedor.query.all()]
    form.proveedores.data = [p.id for p in producto.proveedores]

    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.descripcion = form.descripcion.data
        producto.cantidad = form.cantidad.data
        producto.precio = form.precio.data
        producto.ubicacion = form.ubicacion.data
        producto.referencia = form.referencia.data
        producto.color = form.color.data
        producto.proveedores = Proveedor.query.filter(Proveedor.id.in_(form.proveedores.data)).all()

        db.session.commit()
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('main.listar_productos'))

    return render_template('productos/formulario.html', form=form, titulo='Editar Producto')


@main.route('/producto/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('main.listar_productos'))



# Proveedores
@main.route('/proveedores')
@login_required
def listar_proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores/listar.html', proveedores=proveedores)

@main.route('/proveedor/nuevo', methods=['GET', 'POST'])
@login_required
def crear_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        proveedor = Proveedor(
            nombre_empresa=form.nombre_empresa.data,
            cif=form.cif.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data,
            email=form.email.data,
            descuento=form.descuento.data,
            iva=form.iva.data,
            precio_base=form.precio_base.data
        )
        db.session.add(proveedor)
        db.session.commit()
        flash('Proveedor creado correctamente.', 'success')
        return redirect(url_for('main.listar_proveedores'))
    
    return render_template('proveedores/formulario.html', form=form, titulo='Nuevo Proveedor')

@main.route('/proveedor/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm(obj=proveedor)

    if form.validate_on_submit():
        proveedor.nombre_empresa = form.nombre_empresa.data
        proveedor.cif = form.cif.data
        proveedor.telefono = form.telefono.data
        proveedor.direccion = form.direccion.data
        proveedor.email = form.email.data
        proveedor.descuento = form.descuento.data
        proveedor.iva = form.iva.data
        proveedor.precio_base = form.precio_base.data

        db.session.commit()
        flash('Proveedor actualizado correctamente.', 'success')
        return redirect(url_for('main.listar_proveedores'))

    return render_template('proveedores/formulario.html', form=form, titulo='Editar Proveedor')


@main.route('/proveedor/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado correctamente.', 'success')
    return redirect(url_for('main.listar_proveedores'))

# GraficaAdmin
@main.route('/estadisticas')
@login_required
def estadisticas():
    if current_user.rol != 'admin':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('main.home'))

    proveedores = Proveedor.query.all()
    data = []

    for proveedor in proveedores:
        total_vendido = 0
        beneficio_total = 0

        for producto in proveedor.productos:
            ventas = Venta.query.filter_by(producto_id=producto.id).all()
            for venta in ventas:
                total_vendido += venta.cantidad
                beneficio = (producto.precio - proveedor.precio_base) * venta.cantidad
                beneficio_total += beneficio

        data.append({
            'proveedor': proveedor.nombre_empresa,
            'ventas': total_vendido,
            'beneficio': round(beneficio_total, 2)
        })

    return render_template('estadisticas-admin.html', datos=data)

# GraficaComprasCliente
@main.route('/mis-ventas')
@login_required
def mis_ventas():
    ventas = Venta.query.all()

    ventas_por_dia = {}
    for venta in ventas:
        fecha = venta.fecha.strftime('%Y-%m-%d')
        ventas_por_dia[fecha] = ventas_por_dia.get(fecha, 0) + venta.precio_total

    labels = list(ventas_por_dia.keys())
    valores = list(ventas_por_dia.values())

    return render_template('cliente/estadisticas.html', labels=labels, valores=valores)

#Ruta para añadir productos al carrito
@main.route('/añadir/<int:producto_id>', methods=['POST'])
@login_required
def añadir_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    cantidad = int(request.form.get('cantidad',1))
    
    if cantidad > producto.cantidad:
        flash('❌ No hay suficiente stock disponible.', 'danger')
        return redirect(url_for('main.catalogo'))
    
    carrito = session.get('carrito',{})
    if str(producto_id) in carrito:
        carrito[str(producto_id)] += cantidad
    else:
        carrito[str(producto_id)] = cantidad
        
    session['carrito'] = carrito
    flash(f'🛒 {producto.nombre} añadido al carrito.', 'success')
    return redirect(url_for('main.catalogo'))

#Ruta para ver lo que contiene el carrito
@main.route('/carrito')
@login_required
def ver_carrito():
    carrito = session.get('carrito',{})
    productos = []
    total = 0
    for producto_id,cantidad in carrito.items():
        prod = Producto.query.get(int(producto_id))
        productos.append({
            'producto': prod,
            'cantidad': cantidad,
            'subtotal':prod.precio * cantidad
        })
        total += prod.precio * cantidad

    return render_template('cliente/carrito.html',productos = productos, total=total)

#Ruta para eliminar items del carrito
@main.route('/eliminar/<int:producto_id>',methods=['POST'])
@login_required
def eliminar_del_carrito(producto_id):
    carrito = session.get('carrito',{})
    producto = Producto.query.get_or_404(producto_id)
    if str(producto_id) in carrito:
        carrito.pop(str(producto_id))
        session['carrito'] = carrito
        flash(f'🗑️ {producto.nombre} eliminado correctamente del carrito','info')
    else:
        flash('⚠️ El producto no estaba en el carrito.', 'warning')
        
    return redirect(url_for('main.ver_carrito'))

#Ruta para confirmar la compra
@main.route('/confirmar',methods=['POST'])
@login_required
def confirmar_compra():
    carrito = session.get('carrito',{})
    
    if not carrito:
        flash('🛒 Tu carrito está vacío.','warning')
        return redirect(url_for('main.ver_carrito'))
    
    productos = []
    total = 0
    
    for producto_id, cant in carrito.items():
        producto = Producto.query.get(int(producto_id))
        cantidad = cant | 1
        
        if not producto:
            flash(f'❌ Producto con ID {producto_id} no encontrado.','danger')
            return redirect(url_for('main.ver_carrito'))
        if cantidad > producto.cantidad:
            flash(f'⚠️ No hay suficiente stock para {producto.nombre}.', 'warning')
            return redirect(url_for('main.ver_carrito'))
        
        productos.append((producto,cantidad))
        total += producto.precio * cantidad
        
    for producto,cantidad in productos:
        producto.cantidad -= cantidad
        db.session.add(producto)
        venta = Venta(
            producto_id = producto_id,
            usuario_id = current_user.id,
            cantidad = cantidad,
            fecha = datetime.now(timezone.utc),
            precio_total = producto.precio * cantidad
        )
        db.session.add(venta)
    db.session.commit()
    
    session['carrito'] = {}
    flash('✅ Compra realizada con éxito.', 'success')
    return redirect(url_for('main.mis_ventas'))
    