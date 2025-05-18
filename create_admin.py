from app import create_app, db
from app.models import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    admin = Usuario.query.filter_by(email="admin@email.com").first()
    if not admin:
        novo = Usuario(
            nome="Administrador",
            email="admin@email.com",
            senha=generate_password_hash("admin123")
        )
        db.session.add(novo)
        db.session.commit()
        print("✅ Admin criado com sucesso.")
    else:
        print("ℹ️ Admin já existe.")
