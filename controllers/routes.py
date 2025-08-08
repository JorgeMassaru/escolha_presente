from flask import render_template, request, redirect, url_for
# Importando o Model
from models.database import db, Presente

jogadores = []

gamelist = [{'titulo': 'CS-GO',
             'ano': 2012,
             'categoria': 'FPS Online'}]
  
def init_app(app):
    @app.route('/')
    def home():
        return render_template('presentes.html')

    @app.route('/games', methods=['GET', 'POST'])
    def games():
        game = gamelist[0]
        if request.method == 'POST':
            if request.form.get('jogador'):
                jogadores.append(request.form.get('jogador'))
                return redirect(url_for('games'))
        return render_template('games.html', game=game, jogadores=jogadores)
    
    @app.route('/cadgames', methods=['GET', 'POST'])
    def cadgames():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            gamelist.append(form_data)
            return redirect(url_for('cadgames'))
        return render_template('cadgames.html', gamelist=gamelist)
    
    # API de presentes usando banco SQLite
    @app.route('/presentes', methods=['GET', 'POST'])
    @app.route('/presentes/<int:id>', methods=['GET', 'POST'])
    def apipresentes(id=None):
        if id:
            presente = Presente.query.get(id)
            if presente:
                return render_template('gameinfo.html', ginfo=presente)
            else:
                return f'Presente com a ID {id} não foi encontrado.'
        else:
            presentes = Presente.query.all()
            return render_template('presentes.html', gamesjson=presentes)
    
    # Rota com CRUD de presentes
    @app.route('/estoque', methods=['GET', 'POST'])
    def estoque():
        if request.method == 'POST':
            # Cadastra um novo presente 
            newpresente = Presente(
                request.form['titulo'],
                request.form['categoria'],
                request.form['imagem']
            )
            db.session.add(newpresente)
            db.session.commit()
            return redirect(url_for('estoque'))
        
        # Listar todos os presentes
        presenteestoque = Presente.query.all()
        return render_template('estoque.html', presenteestoque=presenteestoque)
