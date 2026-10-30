import os
from flask import Flask
from database import db
from flask_login import LoginManager
from models.user import User
from routes.auth import auth_bp
from routes.meal import meal_bp
from flasgger import Swagger

app = Flask(__name__, instance_relative_config=True)

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

app.config['SECRET_KEY'] = 'chave_secreta_para_desenvolvimento'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'daily_diet.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configuração personalizada do Swagger (Versão 2.0 obrigatória)
template = {
    "swagger": "2.0",
    "info": {
        "title": "Daily Diet API",
        "description": "API RESTful desenvolvida em Flask para o controle e gestão de rotinas alimentares e métricas de dieta.",
        "contact": {
            "responsibleOrganization": "Gleice Avelino - Desenvolvedora Full Stack",
            "email": "gleiceavelinotech@gmail.com"
        },
        "version": "1.0.0"
    },
    "host": "127.0.0.1:5000",
    "basePath": "/", 
    "schemes": [
        "http"
    ],
}

swagger = Swagger(app, template=template)

app.register_blueprint(auth_bp)
app.register_blueprint(meal_bp)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)