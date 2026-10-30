🥗 Daily Diet API

Uma API RESTful desenvolvida em Python com Flask para gerenciamento e controle de dieta diária. A aplicação permite registrar refeições, listar histórico, calcular métricas de adesão, atualizar e deletar registros, garantindo controle de acesso e isolamento de dados por usuário.

🛠️ Tecnologias Utilizadas

Python 3.10+

Flask: Microframework web para construção de APIs.

Flask-SQLAlchemy: ORM para mapeamento de banco de dados relacional.

Flask-Login: Gerenciamento de sessões e autenticação de usuários.

SQLite: Banco de dados relacional (salvo localmente na pasta instance/).

Werkzeug: Utilitários para hashing seguro de senhas (bcrypt).

📁 Estrutura do Projeto

daily_diet/
├── .gitignore               # Arquivos ignorados pelo Git (venv, instance, caches)
├── requirements.txt         # Dependências do projeto
├── database.py              # Instância global do SQLAlchemy
├── app.py                   # Ponto de entrada e configuração do Flask
├── instance/                # Gerenciado pelo Flask 
│   └── daily_diet.db        # Banco de dados SQLite
├── models/                  # Camada de Dados (ORM)
│   ├── __init__.py
│   ├── user.py              # Modelo de Usuário
│   └── meal.py              # Modelo de Refeição
└── routes/                  # Camada de Controladores / Rotas (Blueprints)
    ├── __init__.py
    ├── auth.py              # Rotas de cadastro e login
    └── meal.py              # Rotas do CRUD e métricas de refeições


🚀 Como Rodar o Projeto Localmente

Pré-requisitos

Python 3.10 ou superior instalado.

Git instalado.

Passo a Passo

Clonar o repositório:

git clone https://github.com/seu-usuario/daily-diet.git
cd daily-diet


Criar e ativar o Ambiente Virtual (venv):

Linux/macOS:

python3 -m venv .venv
source .venv/bin/activate


Windows (PowerShell):

python -m venv .venv
.\.venv\Scripts\Activate.ps1


Instalar as dependências:

pip install -r requirements.txt


Executar a aplicação:

python app.py


A API estará rodando em: http://127.0.0.1:5000

🔐 Autenticação e Segurança

Segurança de Senhas: As senhas são criptografadas com generate_password_hash da Werkzeug antes de serem persistidas no banco.

Controle de Acesso: Todas as rotas de /api/meals são protegidas com a anotação @login_required.

Isolamento de Dados (Anti-IDOR): As consultas de leitura, atualização, deleção e métricas garantem que o registro pertença ao current_user.id.

🌐 Especificação da API (Endpoints)

🔑 Autenticação (/api/auth)

1. Criar Usuário

URL: /api/auth/register

Método: POST

Corpo da Requisição (JSON):

{
  "username": "maria",
  "password": "senha_segura_123"
}


Respostas:

201 Created: Usuário cadastrado com sucesso.

400 Bad Request: Usuário já existe ou campos ausentes.

2. Realizar Login

URL: /api/auth/login

Método: POST

Corpo da Requisição (JSON):

{
  "username": "maria",
  "password": "senha_segura_123"
}


Respostas:

200 OK: Login realizado com sucesso (Sessão iniciada em Cookie).

401 Unauthorized: Credenciais inválidas.

3. Realizar Logout

URL: /api/auth/logout

Método: POST

Requer Autenticação: Sim (@login_required)

Respostas:

200 OK: Sessão encerrada.

🍽️ Refeições (/api/meals)

1. Registrar Refeição

URL: /api/meals

Método: POST

Requer Autenticação: Sim

Corpo da Requisição (JSON):

{
  "name": "Almoço Balanceado",
  "description": "Arroz integral, frango grelhado e salada verde",
  "date_time": "2026-04-12T12:30:00",
  "is_in_diet": true
}


Respostas:

201 Created: Refeição registrada.

400 Bad Request: Campos obrigatórios ausentes.

2. Listar Refeições do Usuário

URL: /api/meals

Método: GET

Requer Autenticação: Sim

Respostas:

200 OK: Retorna a lista de refeições pertencentes ao usuário logado.

3. Obter Métricas e Estatísticas (Dashboard)

URL: /api/meals/metrics

Método: GET

Requer Autenticação: Sim

Respostas:

200 OK: Retorna as estatísticas agregadas do usuário logado.

{
  "total_meals": 10,
  "in_diet_count": 8,
  "out_diet_count": 2,
  "adherence_percentage": 80.0
}


4. Visualizar Refeição Específica

URL: /api/meals/<id>

Método: GET

Requer Autenticação: Sim

Respostas:

200 OK: Retorna os detalhes da refeição.

404 Not Found: Refeição não existe ou não pertence ao usuário.

5. Atualizar Refeição

URL: /api/meals/<id>

Método: PUT

Requer Autenticação: Sim

Corpo da Requisição (JSON):

{
  "name": "Almoço Ajustado",
  "description": "Adicionado azeite de oliva",
  "is_in_diet": true
}


Respostas:

200 OK: Refeição atualizada.

404 Not Found: Refeição não encontrada.

6. Deletar Refeição

URL: /api/meals/<id>

Método: DELETE

Requer Autenticação: Sim

Respostas:

200 OK: Refeição deletada.

404 Not Found: Refeição não encontrada.
