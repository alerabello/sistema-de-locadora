from app import db
from app.models import Filme
from run import app

filmes_exemplo = [
    {
        "titulo": "Interestelar",
        "ano": 2014,
        "cartaz_url": "https://m.media-amazon.com/images/I/71n58PKBFiL._AC_UF894,1000_QL80_.jpg"
    },
    {
        "titulo": "O Poderoso Chefão",
        "ano": 1972,
        "cartaz_url": "https://m.media-amazon.com/images/I/81lZMFwwg5L._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "titulo": "Batman: O Cavaleiro das Trevas",
        "ano": 2008,
        "cartaz_url": "https://m.media-amazon.com/images/I/71pH5SxCRWL._AC_UF894,1000_QL80_.jpg"
    },
    {
        "titulo": "Forrest Gump",
        "ano": 1994,
        "cartaz_url": "https://m.media-amazon.com/images/I/61coc7ZMJyL._AC_UF1000,1000_QL80_.jpg"
    },
    {
        "titulo": "Matrix",
        "ano": 1999,
        "cartaz_url": "https://m.media-amazon.com/images/I/81w+4xkUQdL._AC_UF894,1000_QL80_.jpg"
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
