from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Usuario, Cliente, Filme, Locacao, LocacaoFilme
from .forms import LoginForm, CadastroForm, ClienteForm, LocacaoForm
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    filmes = Filme.query.filter_by(disponivel=True).all()
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
    return render_template('login.html', form=form, show_back_button=True)

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
    return render_template('cadastro.html', form=form, show_back_button=True)

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
        return render_template('filmes.html', filmes=filmes, show_back_button=True)

@main.route('/usuarios')
@login_required
def usuarios():
    if not current_user.is_admin:
        abort(403)
    lista = Usuario.query.all()
    return render_template('usuarios.html', usuarios=lista, show_back_button=True)

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
    return render_template('clientes.html', clientes=lista, show_back_button=True)

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
    return render_template('locacoes.html', locacoes=lista, show_back_button=True)

@main.route('/locacoes/nova', methods=['GET', 'POST'])
@login_required
def nova_locacao():
    if not current_user.is_admin:
        abort(403)
    form = LocacaoForm()
    form.cliente.choices = [(c.id, c.nome) for c in Cliente.query.all()]
    form.filmes.choices = [(f.id, f.titulo) for f in Filme.query.filter_by(disponivel=True).all()]
    if form.validate_on_submit():
        nova = Locacao(cliente_id=form.cliente.data, data_devolucao=form.data_devolucao.data)
        db.session.add(nova)
        db.session.commit()
        for filme_id in form.filmes.data:
            db.session.add(LocacaoFilme(locacao_id=nova.id, filme_id=filme_id))
        db.session.commit()
        flash("Locação registrada com sucesso.")
        return redirect(url_for('main.locacoes'))
    return render_template('locacao_form.html', form=form, titulo="Nova Locação")

@main.route('/locacoes/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_locacao(id):
    if not current_user.is_admin:
        abort(403)
    locacao = Locacao.query.get_or_404(id)
    form = LocacaoForm()
    form.cliente.choices = [(c.id, c.nome) for c in Cliente.query.all()]
    form.filmes.choices = [(f.id, f.titulo) for f in Filme.query.all()]
    if request.method == 'GET':
        form.cliente.data = locacao.cliente_id
        form.data_devolucao.data = locacao.data_devolucao
        form.filmes.data = [lf.filme_id for lf in locacao.filmes]
    if form.validate_on_submit():
        locacao.cliente_id = form.cliente.data
        locacao.data_devolucao = form.data_devolucao.data
        db.session.query(LocacaoFilme).filter_by(locacao_id=locacao.id).delete()
        for filme_id in form.filmes.data:
            db.session.add(LocacaoFilme(locacao_id=locacao.id, filme_id=filme_id))
        db.session.commit()
        flash("Locação atualizada com sucesso.")
        return redirect(url_for('main.locacoes'))
    return render_template('locacao_form.html', form=form, titulo="Editar Locação")

@main.route('/locacoes/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_locacao(id):
    if not current_user.is_admin:
        abort(403)
    locacao = Locacao.query.get_or_404(id)
    db.session.delete(locacao)
    db.session.commit()
    flash("Locação excluída com sucesso.")
    return redirect(url_for('main.locacoes'))

@main.route('/filmes')
@login_required
def listar_filmes():
    if not current_user.is_admin:
        abort(403)
    filmes = Filme.query.all()
    return render_template('filmes_admin.html', filmes=filmes, show_back_button=True)

@main.route('/filmes/novo', methods=['GET', 'POST'])
@login_required
def novo_filme():
    if not current_user.is_admin:
        abort(403)
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        ano = request.form.get('ano')
        cartaz_url = request.form.get('cartaz_url')
        if titulo and ano and cartaz_url:
            filme = Filme(titulo=titulo, ano=ano, disponivel=True, cartaz_url=cartaz_url)
            db.session.add(filme)
            db.session.commit()
            flash("Filme cadastrado com sucesso.")
            return redirect(url_for('main.dashboard'))
        else:
            flash("Preencha todos os campos.")
    return render_template('novo_filme.html', titulo="Novo Filme", show_back_button=True)

@main.route('/filmes/<int:id>/excluir')
@login_required
def excluir_filme(id):
    if not current_user.is_admin:
        abort(403)
    filme = Filme.query.get_or_404(id)
    db.session.delete(filme)
    db.session.commit()
    flash("Filme excluído com sucesso.")
    return redirect(url_for('main.listar_filmes'))

@main.route('/locar', methods=['POST'])
@login_required
def locar_filme_usuario():
    if current_user.is_admin:
        abort(403)
    filmes_ids = request.form.getlist('filmes')
    data_devolucao = request.form.get('data_devolucao')
    if not filmes_ids or not data_devolucao:
        flash("Selecione pelo menos um filme e informe a data de devolução.")
        return redirect(url_for('main.dashboard'))
    # Cria cliente se não existir
    cliente = Cliente.query.filter_by(email=current_user.email).first()
    if not cliente:
        cliente = Cliente(nome=current_user.nome, email=current_user.email)
        db.session.add(cliente)
        db.session.commit()
    # Cria locação
    locacao = Locacao(
        cliente_id=cliente.id,
        data_devolucao=datetime.strptime(data_devolucao, "%Y-%m-%d")
    )
    db.session.add(locacao)
    db.session.commit()
    for filme_id in filmes_ids:
        db.session.add(LocacaoFilme(locacao_id=locacao.id, filme_id=int(filme_id)))
    db.session.commit()
    flash("Locação realizada com sucesso.")
    return redirect(url_for('main.dashboard'))

@main.cli.command("seed_filmes")
def seed_filmes():
    exemplos = [
        {"titulo": "O Poderoso Chefão", "ano": 1972, "cartaz_url": "https://m.media-amazon.com/images/I/71xBLRBYOiL._AC_SY679_.jpg"},
        {"titulo": "Interestelar", "ano": 2014, "cartaz_url": "https://m.media-amazon.com/images/I/91kFYg4fX3L._AC_SY679_.jpg"},
        {"titulo": "Clube da Luta", "ano": 1999, "cartaz_url": "https://m.media-amazon.com/images/I/81D+KJkO6-L._AC_SY679_.jpg"},
        {"titulo": "Forrest Gump", "ano": 1994, "cartaz_url": "https://m.media-amazon.com/images/I/61OUGpUfAyL._AC_SY679_.jpg"},
        {"titulo": "A Origem", "ano": 2010, "cartaz_url": "https://m.media-amazon.com/images/I/81p+xe8cbnL._AC_SY679_.jpg"},
    ]
    for f in exemplos:
        filme = Filme(titulo=f["titulo"], ano=f["ano"], cartaz_url=f["cartaz_url"], disponivel=True)
        db.session.add(filme)
    db.session.commit()
    print("🎉 Filmes de exemplo adicionados com sucesso.")