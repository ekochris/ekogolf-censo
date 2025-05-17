# reset_database.py

import os
from app import create_app, db

app = create_app()

with app.app_context():
    db_path = os.path.join(os.getcwd(), 'data.db')

    # Eliminar base de datos si existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Archivo 'data.db' eliminado correctamente.")
    else:
        print("⚠️ El archivo 'data.db' no existe o ya fue eliminado.")

    # Crear nueva base de datos vacía
    db.create_all()
    print("✅ Nueva base de datos creada con éxito.")
