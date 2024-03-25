import os
from jogoteca import app
from flask_wtf import FlaskForm # serve para validação de formulario
from wtforms import StringField, SubmitField, validators #validators serve para validar se tem dado

class FormularioJogo(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.length(min=1, max=50)])
    categoria = StringField('Categoria', [validators.DataRequired(), validators.length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.length(min=1, max=20)])
    salvar = SubmitField('Salvar')

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo: #contains do javascript
            return nome_arquivo
    return 'sample.png'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo !='sample.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))