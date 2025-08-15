from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default='user')  # 'user' ou 'admin'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Presente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    categoria = db.Column(db.String(150))
    imagem = db.Column(db.String(300))
    escolhido = db.Column(db.Boolean, default=False)
    escolhido_por = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Quem escolheu

    def __init__(self, titulo, categoria, imagem):
        self.titulo = titulo
        self.categoria = categoria
        self.imagem = imagem
