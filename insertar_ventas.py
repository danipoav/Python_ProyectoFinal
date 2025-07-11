from app import create_app, db
from app.models import Producto, Usuario, Venta
from datetime import datetime, timezone, timedelta
import random

app = create_app()

with app.app_context():
    productos = Producto.query.all()
    usuario = Usuario.query.first()  

    if not productos:
        print("⚠️ No hay productos en la base de datos. Añade alguno primero.")
    elif not usuario:
        print("⚠️ No hay usuarios en la base de datos. Añade uno primero.")
    else:
        for i in range(15): 
            producto = random.choice(productos)
            cantidad = random.randint(1, 5)
            precio_total = producto.precio * cantidad
            fecha = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 14))

            venta = Venta(
                producto_id=producto.id,
                usuario_id=usuario.id,
                cantidad=cantidad,
                precio_total=precio_total,
                fecha=fecha
            )
            db.session.add(venta)

        db.session.commit()
        print("✅ Ventas de prueba insertadas correctamente.")
