from . import db
from flask_login import UserMixin
from datetime import datetime,timezone

producto_proveedor = db.Table('producto_proveedor',
    db.Column('producto_id', db.Integer, db.ForeignKey('producto.id')),
    db.Column('proveedor_id', db.Integer, db.ForeignKey('proveedor.id'))
)

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='cliente')

    def __repr__(self):
        return f'<Usuario {self.nombre}>'


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    cantidad = db.Column(db.Integer, nullable=False)
    stock_maximo = db.Column(db.Integer, nullable=False, default=100) 
    precio = db.Column(db.Float, nullable=False)
    ubicacion = db.Column(db.String(100))
    referencia = db.Column(db.String(100))
    color = db.Column(db.String(50))
    proveedores = db.relationship('Proveedor', secondary=producto_proveedor, backref='productos')

    def __repr__(self):
        return f'<Producto {self.nombre} - Stock: {self.cantidad}>'


class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_empresa = db.Column(db.String(150), nullable=False)
    cif = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(200))
    email = db.Column(db.String(150))
    descuento = db.Column(db.Float, default=0.0)
    iva = db.Column(db.Float, default=21.0)
    precio_base = db.Column(db.Float)

    def __repr__(self):
        return f'<Proveedor {self.nombre_empresa}>'
    
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    precio_total = db.Column(db.Float, nullable=False)

    producto = db.relationship('Producto', backref='ventas')
    usuario = db.relationship('Usuario', backref='ventas')

    def __repr__(self):
        return f'<Venta {self.producto.nombre} x {self.cantidad} - {self.fecha.strftime("%Y-%m-%d")}>'

