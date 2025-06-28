from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SelectMultipleField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets import ListWidget, CheckboxInput

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar login')
    submit = SubmitField('Entrar')

class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Cadastrar')

class ClienteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone')
    submit = SubmitField('Salvar')

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class LocacaoForm(FlaskForm):
    cliente = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    filmes = MultiCheckboxField('Filmes', coerce=int, validators=[DataRequired()])
    data_devolucao = DateField('Data de Devolução', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Salvar')

class PerfilForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Salvar')