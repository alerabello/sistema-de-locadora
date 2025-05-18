from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Usuario, Cliente, Filme, Locacao, LocacaoFilme
from .forms import LoginForm, CadastroForm, ClienteForm, LocacaoForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    filmes = Filme.query.filter_by(disponivel=True).limit(3).all()
    return render_template('index.html', filmes=filmes)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and check_password_hash(usuario.senha, form.senha.data):
            login_user(usuario, remember=form.lembrar.data)
            return redirect(url_for('main.dashboard'))
        flash('Login inválido')
    return render_template('login.html', form=form)

@main.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = CadastroForm()
    if request.method == 'POST' and form.validate_on_submit():
        if Usuario.query.filter_by(email=form.email.data).first():
            flash('Email já cadastrado. Faça login.')
            return redirect(url_for('main.login'))
        novo = Usuario(
            nome=form.nome.data,
            email=form.email.data,
            senha=generate_password_hash(form.senha.data),
            is_admin=False
        )
        db.session.add(novo)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça login.')
        return redirect(url_for('main.login'))
    return render_template('cadastro.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return render_template('dashboard.html')
    else:
        filmes = Filme.query.filter_by(disponivel=True).all()
        return render_template('filmes.html', filmes=filmes)

@main.route('/usuarios')
@login_required
def usuarios():
    if not current_user.is_admin:
        abort(403)
    lista = Usuario.query.all()
    return render_template('usuarios.html', usuarios=lista)

@main.route('/usuarios/<int:id>/promover')
@login_required
def promover_usuario(id):
    if not current_user.is_admin:
        abort(403)
    usuario = Usuario.query.get_or_404(id)
    usuario.is_admin = True
    db.session.commit()
    flash("Usuário promovido a administrador.")
    return redirect(url_for('main.usuarios'))

@main.route('/usuarios/<int:id>/rebaixar')
@login_required
def rebaixar_usuario(id):
    if not current_user.is_admin:
        abort(403)
    usuario = Usuario.query.get_or_404(id)
    usuario.is_admin = False
    db.session.commit()
    flash("Permissões de administrador removidas.")
    return redirect(url_for('main.usuarios'))

@main.route('/clientes')
@login_required
def clientes():
    if not current_user.is_admin:
        abort(403)
    lista = Cliente.query.all()
    return render_template('clientes.html', clientes=lista)

@main.route('/clientes/novo', methods=['GET', 'POST'])
@login_required
def novo_cliente():
    if not current_user.is_admin:
        abort(403)
    form = ClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(nome=form.nome.data, email=form.email.data, telefone=form.telefone.data)
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente cadastrado com sucesso.")
        return redirect(url_for('main.clientes'))
    return render_template('cliente_form.html', form=form, titulo="Novo Cliente")

@main.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_cliente(id):
    if not current_user.is_admin:
        abort(403)
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        cliente.nome = form.nome.data
        cliente.email = form.email.data
        cliente.telefone = form.telefone.data
        db.session.commit()
        flash("Cliente atualizado com sucesso.")
        return redirect(url_for('main.clientes'))
    return render_template('cliente_form.html', form=form, titulo="Editar Cliente")

@main.route('/clientes/<int:id>/excluir')
@login_required
def excluir_cliente(id):
    if not current_user.is_admin:
        abort(403)
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente excluído com sucesso.")
    return redirect(url_for('main.clientes'))

@main.route('/locacoes')
@login_required
def locacoes():
    if not current_user.is_admin:
        abort(403)
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
        flash("Locação registrada com sucesso.")
        return redirect(url_for('main.locacoes'))

    return render_template('locacao_form.html', form=form, titulo="Nova Locação")

@main.route('/locacoes/<int:id>/excluir')
@login_required
def excluir_locacao(id):
    if not current_user.is_admin:
        abort(403)
    locacao = Locacao.query.get_or_404(id)
    for item in locacao.filmes:
        item.filme.disponivel = True
        db.session.delete(item)
    db.session.delete(locacao)
    db.session.commit()
    flash("Locação excluída com sucesso.")
    return redirect(url_for('main.locacoes'))

@main.route('/filmes/novo', methods=['GET', 'POST'])
@login_required
def novo_filme():
    if not current_user.is_admin:
        abort(403)

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        ano = request.form.get('ano')
        if titulo and ano:
            filme = Filme(titulo=titulo, ano=ano, disponivel=True)
            db.session.add(filme)
            db.session.commit()
            flash("Filme cadastrado com sucesso.")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Preencha todos os campos.")
    return render_template('novo_filme.html')
