from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    locacoes = db.relationship('Locacao', backref='cliente', lazy=True)

class Filme(db.Model):
    __tablename__ = 'filmes'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    genero = db.Column(db.String(50))
    ano = db.Column(db.Integer)
    disponivel = db.Column(db.Boolean, default=True)
    cartaz_url = db.Column(db.String(255), nullable=True)


class Locacao(db.Model):
    __tablename__ = 'locacoes'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_locacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_devolucao = db.Column(db.DateTime, nullable=True)
    filmes = db.relationship('LocacaoFilme', backref='locacao', cascade="all, delete-orphan")

class LocacaoFilme(db.Model):
    __tablename__ = 'locacoes_filmes'
    id = db.Column(db.Integer, primary_key=True)
    locacao_id = db.Column(db.Integer, db.ForeignKey('locacoes.id'), nullable=False)
    filme_id = db.Column(db.Integer, db.ForeignKey('filmes.id'), nullable=False)
    filme = db.relationship('Filme')