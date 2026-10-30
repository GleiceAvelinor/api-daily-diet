from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from database import db
from models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registar um novo utilizador
    ---
    tags:
      - Autenticação
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: gleice_avelino
            password:
              type: string
              example: senhaSegura123
    responses:
      201:
        description: Utilizador registado com sucesso
      400:
        description: Utilizador já existe ou campos em falta
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username e password são obrigatórios"}), 400

    user_exists = User.query.filter_by(username=username).first()
    if user_exists:
        return jsonify({"message": "Usuário já existe"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autenticar o utilizador e iniciar sessão
    ---
    tags:
      - Autenticação
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: gleice_avelino
            password:
              type: string
              example: senhaSegura123
    responses:
      200:
        description: Login realizado com sucesso
      401:
        description: Credenciais inválidas
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({"message": "Login realizado com sucesso!"}), 200

    return jsonify({"message": "Credenciais inválidas"}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Terminar a sessão do utilizador autenticado
    ---
    tags:
      - Autenticação
    responses:
      200:
        description: Logout realizado com sucesso
      401:
        description: Utilizador não autenticado
    """
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"}), 200