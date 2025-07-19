from app import create_app, db
from app.models import Proveedor, Producto

app = create_app()

with app.app_context():
    proveedor = Proveedor.query.all()
    if not proveedor:
        proveedor1 = Proveedor(
            nombre_empresa="Informática DaniTech",
            cif="B12345678",
            telefono="612345678",
            direccion="Calle Falsa 123",
            email="contacto@danitech.com",
            descuento=10,
            iva=21,
            precio_base=100
        )

        proveedor2 = Proveedor(
            nombre_empresa="Componentes Pro",
            cif="B87654321",
            telefono="698765432",
            direccion="Avenida Siempre Viva 742",
            email="ventas@componentespro.com",
            descuento=5,
            iva=21,
            precio_base=80
        )

        db.session.add_all([proveedor1, proveedor2])
        db.session.commit()

        producto1 = Producto(
            nombre="Monitor 24'' FullHD",
            descripcion="Monitor IPS 24 pulgadas",
            cantidad=10,
            precio=150.0,
            ubicacion="Estantería A1",
            referencia="MON24HD",
            color="Negro",
            stock_maximo=20,
            proveedores=[proveedor1]
        )

        producto2 = Producto(
            nombre="Teclado mecánico RGB",
            descripcion="Teclado con switches rojos y luces RGB",
            cantidad=7,
            precio=60.0,
            ubicacion="Estantería B2",
            referencia="TECRGB",
            color="Blanco",
            stock_maximo=15,
            proveedores=[proveedor2]
        )

        producto3 = Producto(
            nombre="Ratón inalámbrico",
            descripcion="Ratón ergonómico con batería recargable",
            cantidad=12,
            precio=30.0,
            ubicacion="Estantería C3",
            referencia="RATWIRELESS",
            color="Gris",
            stock_maximo=20,
            proveedores=[proveedor1, proveedor2]
        )

        db.session.add_all([producto1, producto2, producto3])
        db.session.commit()

        print("✅ Proveedores y productos de prueba insertados correctamente.")
