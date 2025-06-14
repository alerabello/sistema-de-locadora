# Sistema de Locadora de Filmes 🎬

Este é um sistema web desenvolvido com Flask, seguindo princípios de Engenharia de Software.

## Funcionalidades

- Cadastro e autenticação de usuários
- Gerenciamento de clientes (CRUD)
- Gerenciamento de filmes (CRUD)
- Gerenciamento de locações (CRUD, com múltiplos filmes por locação)
- Interface responsiva com Bootstrap
- Testes automatizados com unittest e Selenium
- Relatórios de locações por período
- Exportação de dados em CSV
- Recuperação de senha por e-mail
- Filtros avançados de busca para filmes e clientes
- Dashboard com estatísticas do sistema

---

## Requisitos Mínimos

- **Python**: 3.8 ou superior
- **Flask**: 2.0 ou superior
- **Bootstrap**: 5.0 ou superior
- **Google Chrome**: 90 ou superior
- **ChromeDriver**: Compatível com a versão do Chrome instalada
- **pip**: 20.0 ou superior
- **Sistema Operacional**: Linux, Windows ou macOS
- **PostgreSQL**: Versão 15 ou superior

---

## Como rodar localmente

### 1. Clone o projeto e crie o ambiente virtual
```bash
git clone https://github.com/seu-usuario/sistema-de-locadora.git
cd sistema-de-locadora
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows