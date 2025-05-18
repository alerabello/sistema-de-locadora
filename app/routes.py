from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Usuario, Cliente, Filme, Locacao, LocacaoFilme
from .forms import LoginForm, CadastroForm, ClienteForm, LocacaoForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    login_form = LoginForm()
    cadastro_form = CadastroForm()

    if login_form.submit.data and login_form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=login_form.email.data).first()
        if usuario and check_password_hash(usuario.senha, login_form.senha.data):
            login_user(usuario, remember=login_form.lembrar.data)
            return redirect(url_for('main.dashboard'))
        flash('Login inválido')

    elif cadastro_form.submit.data and cadastro_form.validate_on_submit():
        if Usuario.query.filter_by(email=cadastro_form.email.data).first():
            flash('Email já cadastrado. Faça login.')
        else:
            novo = Usuario(
                nome=cadastro_form.nome.data,
                email=cadastro_form.email.data,
                senha=generate_password_hash(cadastro_form.senha.data)
            )
            db.session.add(novo)
            db.session.commit()
            flash('Cadastro realizado com sucesso! Faça login.')

    return render_template('index.html', login_form=login_form, cadastro_form=cadastro_form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@main.route('/clientes')
@login_required
def clientes():
    lista = Cliente.query.all()
    return render_template('clientes.html', clientes=lista)

@main.route('/clientes/novo', methods=['GET', 'POST'])
@login_required
def novo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(nome=form.nome.data, email=form.email.data, telefone=form.telefone.data)
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('main.clientes'))
    return render_template('cliente_form.html', form=form, titulo="Novo Cliente")

@main.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        cliente.nome = form.nome.data
        cliente.email = form.email.data
        cliente.telefone = form.telefone.data
        db.session.commit()
        return redirect(url_for('main.clientes'))
    return render_template('cliente_form.html', form=form, titulo="Editar Cliente")

@main.route('/clientes/<int:id>/excluir')
@login_required
def excluir_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for('main.clientes'))

@main.route('/locacoes')
@login_required
def locacoes():
    lista = Locacao.query.all()
    return render_template('locacoes.html', locacoes=lista)

@main.route('/locacoes/nova', methods=['GET', 'POST'])
@login_required
def nova_locacao():
    form = LocacaoForm()
    form.cliente.choices = [(c.id, c.nome) for c in Cliente.query.all()]
    form.filmes.choices = [(f.id, f"{f.titulo} ({f.ano})") for f in Filme.query.filter_by(disponivel=True).all()]

    if form.validate_on_submit():
        locacao = Locacao(
            cliente_id=form.cliente.data,
            data_devolucao=form.data_devolucao.data
        )
        db.session.add(locacao)
        db.session.flush()

        for filme_id in form.filmes.data:
            filme = Filme.query.get(filme_id)
            filme.disponivel = False
            db.session.add(LocacaoFilme(locacao_id=locacao.id, filme_id=filme_id))

        db.session.commit()
        return redirect(url_for('main.locacoes'))

    return render_template('locacao_form.html', form=form, titulo="Nova Locação")

@main.route('/locacoes/<int:id>/excluir')
@login_required
def excluir_locacao(id):
    locacao = Locacao.query.get_or_404(id)
    for item in locacao.filmes:
        item.filme.disponivel = True
        db.session.delete(item)
    db.session.delete(locacao)
    db.session.commit()
    return redirect(url_for('main.locacoes'))