from app import db
from app.models import Usuario
from werkzeug.security import generate_password_hash

admin = Usuario.query.filter_by(email="admin@email.com").first()

if not admin:
    novo_admin = Usuario(
        nome="Administrador",
        email="admin@email.com",
        senha=generate_password_hash("admin123"),
        is_admin=True
    )
    db.session.add(novo_admin)
    db.session.commit()
    print("✅ Usuário administrador criado com sucesso!")
else:
    print("⚠️ Usuário administrador já existe.")
