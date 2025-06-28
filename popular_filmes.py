from app import db
from app.models import Filme
from run import app

filmes_exemplo = [
    {
        "titulo": "Interestelar",
        "ano": 2014,
        "cartaz_url": "https://upload.wikimedia.org/wikipedia/pt/thumb/3/3a/Interstellar_Filme.png/250px-Interstellar_Filme.png"
    },
    {
        "titulo": "O Poderoso Chefão",
        "ano": 1972,
        "cartaz_url": "https://upload.wikimedia.org/wikipedia/pt/d/de/Godfather_1972.jpg"
    },
    {
        "titulo": "Batman: O Cavaleiro das Trevas",
        "ano": 2008,
        "cartaz_url": "https://upload.wikimedia.org/wikipedia/pt/d/d1/The_Dark_Knight.jpg"
    },
    {
        "titulo": "Forrest Gump",
        "ano": 1994,
        "cartaz_url": "https://upload.wikimedia.org/wikipedia/pt/c/c0/ForrestGumpPoster.jpg"
    },
    {
        "titulo": "Matrix",
        "ano": 1999,
        "cartaz_url": "https://upload.wikimedia.org/wikipedia/pt/c/c1/The_Matrix_Poster.jpg"
    }
]

with app.app_context():
    for filme_data in filmes_exemplo:
        existe = Filme.query.filter_by(titulo=filme_data["titulo"]).first()
        if not existe:
            novo = Filme(
                titulo=filme_data["titulo"],
                ano=filme_data["ano"],
                disponivel=True,
                cartaz_url=filme_data["cartaz_url"]
            )
            db.session.add(novo)
    db.session.commit()
    print("✅ Filmes adicionados com sucesso.")
