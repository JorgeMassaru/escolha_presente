from flask_sqlalchemy import SQLAlchemy 

#Criando uma instância do SQLAlchemy
db = SQLAlchemy()

#Classe responsável por criar a entidade "Games" no banco com seus atributos
class Presente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    categoria = db.Column(db.String(150))
    imagem = db.Column(db.String(300))
    escolhido = db.Column(db.Boolean, default=False)  # novo campo

    def __init__(self, titulo, categoria, imagem):
        self.titulo = titulo
        self.categoria = categoria
        self.imagem = imagem
