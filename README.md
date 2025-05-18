```markdown
# Sistema de Locadora de Filmes 🎬

Este é um sistema web desenvolvido com Flask, seguindo princípios de Engenharia de Software.

## Funcionalidades

- Cadastro e autenticação de usuários
- Gerenciamento de clientes (CRUD)
- Gerenciamento de filmes (CRUD)
- Gerenciamento de locações (CRUD, com múltiplos filmes por locação)
- Interface responsiva com Bootstrap
- Testes automatizados com unittest e Selenium

## Como rodar localmente

### 1. Clone o projeto e crie o ambiente virtual
```bash
git clone https://github.com/seu-usuario/sistema-de-locadora.git
cd sistema-de-locadora
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Inicie o banco de dados
```bash
python run.py
```
O banco será criado automaticamente na primeira execução.

### 4. Crie um usuário admin
```bash
python create_admin.py
```
Login padrão: `admin@email.com`  
Senha padrão: `admin123`

### 5. Acesse o sistema
Abra no navegador: http://localhost:5000

---

## Executar Testes

### Testes Unitários
```bash
python -m unittest discover tests
```

### Testes de Integração com Selenium
Certifique-se de que o ChromeDriver está instalado e no PATH.
```bash
python tests/test_selenium.py
```

---

## Requisitos

- Python 3.8+
- Google Chrome + ChromeDriver (para testes Selenium)
- Flask 2.x
- Bootstrap 5

---
```