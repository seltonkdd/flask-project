from flask import Flask, render_template, request, redirect, url_for, flash
from db import create_database, salvar_database, get_database, delete_and_save, get_user_by_id
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from models import User
import hashlib

app = Flask(__name__)
app.config['DEBUG'] = True
lm = LoginManager(app)
app.secret_key = 'supersecretkey'

@lm.user_loader
def user_loader(id):
    user = get_user_by_id(id)
    if user:
        return User(user[0], user[1], user[2], user[3], user[4])
    return None

@app.route('/')
@login_required
def index():
    return render_template('index.html', person=current_user.username)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    logout_user()
    if request.method == 'POST':
        username = request.form['usernameForm']
        email = request.form['emailForm']
        password = request.form['passwordForm']
        salvar_database(username, email, password)

        return redirect(url_for('login'))
    return render_template('registrar.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['emailForm']
        password = request.form['passwordForm']
        db = get_database()
        hash = hashlib.sha256(password.encode()).hexdigest()
        
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, hash)).fetchone()
        db.close()
        if user:
            user_obj = User(user[0], user[1], user[2], user[3], user[4])
            login_user(user_obj)

            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos')
            
            
    return render_template('login.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user.username, email=current_user.email, bio=current_user.bio)

@app.route('/users')
def users():
    db = get_database()
    users = db.execute('SELECT * FROM users').fetchall()
    db.close()
    return {"usuarios": [dict(row) for row in users]}

@app.route('/edit')
def edit_user(id):
    user = get_user_by_id(id)
    return render_template('editar.html')

@app.route('/delete/<int:id>')
def delete_user(id):
    delete_and_save(id)
    return redirect(url_for('users'))

if __name__ == '__main__':
    create_database()
    app.run()