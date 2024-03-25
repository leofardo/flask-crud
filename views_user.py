from jogoteca import app, db
from flask import render_template, request, redirect, session, flash, url_for
from models import Usuarios
from helpers import FormularioUsuario
from flask_bcrypt import check_password_hash

@app.route('/login')
def login():
    proxima = request.args.get('proxima')

    form = FormularioUsuario()

    return render_template('login.html', proxima=proxima, form=form)

@app.route('/autenticar', methods=['POST',])

def autenticar():

    form = FormularioUsuario(request.form)

    #fazendo o select com o ORM SQLALCHEMY
    usuario = Usuarios.query.filter_by(nickname=form.nickname.data).first()
    senha = check_password_hash(usuario.senha, form.senha.data)

    if usuario and senha: #se achar

        session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logado com sucesso!')
        proxima_pagina = request.form['proxima']

        return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha incorretos.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))