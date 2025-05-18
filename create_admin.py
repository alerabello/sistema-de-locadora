from app import db
from app.models import Usuario
from werkzeug.security import generate_password_hash
from run import app  # importa o app de onde ele é instanciado

with app.app_context():
    admin = Usuario.query.filter_by(email="admin@email.com").first()
    if not admin:
        novo = Usuario(
            nome="Administrador",
            email="admin@email.com",
            senha=generate_password_hash("admin123"),
            is_admin=True
        )
        db.session.add(novo)
        db.session.commit()
        print("✅ Admin criado com sucesso")
    else:
        print("⚠️ Admin já existe")
