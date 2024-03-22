import os
from jogoteca import app

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo: #contains do javascript
            return nome_arquivo
    return 'sample.png'

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo !='sample.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))