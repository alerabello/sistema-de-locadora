import unittest
from app import create_app
from app.models import db, Cliente

class ClienteModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_criar_cliente(self):
        cliente = Cliente(nome='João Silva', email='joao@email.com', telefone='999999999')
        db.session.add(cliente)
        db.session.commit()
        resultado = Cliente.query.filter_by(email='joao@email.com').first()
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nome, 'João Silva')