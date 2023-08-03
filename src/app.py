from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_paginate import Pagination, get_page_args
from config import config

# Models:
from models.ModelUser import ModelUser, Cliente, Cotizacion

# Entities:
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # print(request.form['username'])
        # print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                
                return redirect(url_for('home'))
            else:
                flash("Invalid password...")
                return render_template('auth/login.html')
        else:
            flash("User not found...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"

@app.route('/clientes', methods=['GET'])
def clientes():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    
    clientes = Cliente.obtener_todos(db, offset=offset, limit=per_page)
    
    total_clientes = 100
    
    pagination = Pagination(page=page, per_page=per_page, total=total_clientes, css_framework='bootstrap5')
    
    return render_template('clientes.html', clientes=clientes,page=page,pager_page=per_page,pagination=pagination)

@app.route('/cotizaciones', methods=['GET'])
def cotizaciones():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    
    cotizaciones = Cotizacion.obtener_todos(db, offset=offset, limit=per_page)
    
    total_cotizaciones = 100
    
    pagination = Pagination(page=page, per_page=per_page, total=total_cotizaciones, css_framework='bootstrap5')
    
    return render_template('cotizaciones.html', cotizaciones=cotizaciones,page=page,pager_page=per_page,pagination=pagination)

@app.route('/ingresar_cliente', methods=['GET', 'POST'])
def mostrar_formulario_cliente():
    if request.method == 'POST':
        # Obtener los datos ingresados en el formulario
        razon_social = request.form['razon_social']
        rut = request.form['rut']
        telefono = request.form['telefono']
        email = request.form['email']
        persona_de_contacto = request.form['persona_de_contacto']

        # Crear un nuevo objeto Cliente con los datos ingresados
        nuevo_cliente = Cliente(razon_social, rut, telefono, email, persona_de_contacto)

        # Insertar el nuevo cliente en la base de datos
        nuevo_cliente.insertar(db)

        # Redirigir a la página de lista de clientes después de agregar el nuevo cliente
        return redirect(url_for('clientes'))

    return render_template('ingresar_cliente.html')

def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()
