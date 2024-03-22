from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from jogoteca import app, db
from models import Jogos, Usuarios
from helpers import *
import time

@app.route('/')
def index():
    # fazendo o select com o ORM SQLALCHEMY
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():

    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogos.query.filter_by(nome=nome).first()
    print(jogo)
    if jogo:
        flash('Jogo Já existente.')
        return redirect(url_for('novo'))

    #incluindo jogo no db do mysql
    novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(novo_jogo)
    db.session.commit()

    #salvando o arquivo
    arquivo = request.files['arquivo']

    #buscando o diretorio na aba config
    upload_path = app.config['UPLOAD_PATH']

    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{novo_jogo.id}-{timestamp}.png')


    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar', id=id)))

    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recupera_imagem(id)

    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo, capa_jogo=capa_jogo)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])

def autenticar():
    #fazendo o select com o ORM SQLALCHEMY
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()

    if usuario: #se achar
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Senha incorreta.')
            return redirect(url_for('login'))
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

@app.route('/atualizar', methods=['POST',])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()

    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']

    #mesma sintaxe de criar, mas aqui vai atualizar
    db.session.add(jogo)
    db.session.commit()

    # salvando o arquivo
    arquivo = request.files['arquivo']

    # buscando o diretorio na aba config
    upload_path = app.config['UPLOAD_PATH']

    #ajuste no cache
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.png')

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login'))

    #deletando
    Jogos.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Jogo deletado com sucesso')

    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

