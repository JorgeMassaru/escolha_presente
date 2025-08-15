from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from models.database import db, Presente, User
# Importando o Model
from models.database import db, Presente
  
def init_app(app):
    @app.route('/')
    def home():
        return render_template('presentes.html')

    
    @app.route('/cadpresentes', methods=['GET', 'POST'])
    def cadpresentes():
        if request.method == 'POST':
            form_data = request.form.to_dict()
            presentelist.append(form_data)
            return redirect(url_for('cadpresentes'))
        return render_template('cadpresentes.html', presentelist=presentelist)
    
    # API de presentes usando banco SQLite
    @app.route('/presentes', methods=['GET', 'POST'])
    @login_required
    def apipresentes(id=None):
        if request.method == 'POST':
            presente_id = int(request.form['presente_id'])
            action = request.form.get('action', 'escolher')

            presente = Presente.query.get_or_404(presente_id)

            if action == 'escolher' and not presente.escolhido:
                presente.escolhido = True
                presente.escolhido_por = current_user.id
                db.session.commit()

            elif action == 'cancelar' and presente.escolhido and presente.escolhido_por == current_user.id:
                presente.escolhido = False
                presente.escolhido_por = None
                db.session.commit()

            return redirect(url_for('apipresentes'))

        presentes = Presente.query.all()
        return render_template('presentes.html', presentes=presentes)

    
    # Rota com CRUD de presentes
    @app.route('/estoque', methods=['GET', 'POST'])
    @login_required
    def estoque():
        if current_user.role != 'admin':
            return "Acesso negado!", 403

        if request.method == 'POST':
            newpresente = Presente(
                request.form['titulo'],
                request.form['categoria'],
                request.form['imagem']
            )
            db.session.add(newpresente)
            db.session.commit()
            return redirect(url_for('estoque'))

        presenteestoque = Presente.query.all()
        return render_template('estoque.html', presenteestoque=presenteestoque)


    #Rota para Registrar o usuário 
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            if User.query.filter_by(username=username).first():
                flash('Usuário já existe!')
                return redirect(url_for('register'))

            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('Conta criada com sucesso!')
            return redirect(url_for('login'))

        return render_template('register.html')

    #Rota para fazer login no sistema com sistema de hash
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('apipresentes'))
            else:
                flash('Login inválido!')
        return render_template('caduser.html')

    #Rota para fazer o logout
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))
