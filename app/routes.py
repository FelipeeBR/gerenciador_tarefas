from flask import render_template, url_for, redirect, request, session, flash
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from app import app, db
from app.models import User, Tasks


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not name or not email or not password:
            flash('Por favor, preencha todos os campos.', 'error')
            return redirect('/register')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Este e-mail já está cadastrado. Por favor, use outro e-mail.', 'error')
            return redirect('/register')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça o login.', 'success')
        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user) 
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Usuário Inválido')

    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    task_list = Tasks.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user=current_user, task_list=task_list)

@app.route('/dashboard/finalizados')
@login_required
def finalizado():
    task_list = Tasks.query.filter_by(user_id=current_user.id, done=True).all()
    return render_template('finished.html', user=current_user, task_list=task_list)

@app.route('/dashboard/importantes')
@login_required
def important():
    task_list = Tasks.query.filter_by(user_id=current_user.id, important=True).all()
    return render_template('important.html', user=current_user, task_list=task_list)

@app.route('/dashboard/add', methods=['POST'])
def add():
    title = request.form.get('title')
    description = request.form.get('description')
    important = request.form.get('important') == 'on'
    new_task = Tasks(title=title, description=description, important=important, done=False, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/dashboard/update/<int:task_id>')
def update(task_id):
    task = Tasks.query.get(task_id)
    task.done=not task.done
    db.session.commit()
    return redirect('/dashboard')

@app.route('/dashboard/delete/<int:task_id>')
def delete(task_id):
    task = Tasks.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/dashboard')