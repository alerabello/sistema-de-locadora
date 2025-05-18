```markdown
# Sistema de Locadora de Filmes 🎬

Este é um sistema web completo desenvolvido com Flask, utilizando os princípios da Engenharia de Software.

## Funcionalidades

- Cadastro e login de usuários
- CRUD de Clientes
- CRUD de Locações (com múltiplos filmes)
- Interface com Bootstrap
- Testes com PyUnit e Selenium

## Como rodar localmente

### 1. Clone o projeto e crie ambiente virtual
```bash
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

### 4. Crie um usuário admin
```bash
python create_admin.py
```

Login: `admin@email.com`  
Senha: `admin123`

### 5. Acesse o sistema
Abra no navegador: http://localhost:5000

---

## Executar Testes

### Testes Unitários
```bash
python -m unittest discover tests
```

### Testes com Selenium
```bash
python tests/test_selenium.py
```

---

## Requisitos
- Python 3.8+
- Google Chrome + ChromeDriver (para Selenium)
```

---