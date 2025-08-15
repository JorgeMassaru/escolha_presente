from flask import Flask
from flask_login import LoginManager
from controllers import routes
from models.database import db, User  # Você vai criar a model User
import os

# Criando a instancia do Flask
app = Flask(__name__, template_folder='views')

# Chave secreta para sessões
app.secret_key = 'chave_super_secreta_trocar_aqui'

# Inicializa as rotas
routes.init_app(app)

# Caminho do banco
dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/presentes.sqlite3')

# Inicializa o banco
db.init_app(app)

# Configura o Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'  # rota de login obrigatória
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='localhost', port=5000, debug=True)
