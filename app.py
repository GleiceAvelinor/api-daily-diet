import os
from flask import Flask
from database import db
from flask_login import LoginManager
from models.user import User
from routes.auth import auth_bp
from routes.meal import meal_bp

# Configura a aplicação para resolver caminhos relativos dentro da pasta instance/
app = Flask(__name__, instance_relative_config=True)

# Garante que a pasta instance/ exista no sistema de arquivos
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Configurações
app.config['SECRET_KEY'] = 'chave_secreta_para_desenvolvimento'
# Salva o banco dentro de instance/daily_diet.db
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'daily_diet.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização de extensões
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registro de Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(meal_bp)

# Criação das tabelas dentro do escopo da aplicação
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)