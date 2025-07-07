from app import create_app

app = create_app()

# with app.app_context():
#     db.create_all()
#     print("Base de datos creada correctamente.")

if __name__ == '__main__':
    app.run(debug=True)
