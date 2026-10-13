from bicicletario import Bicicleta
from bottle import get, post, request, route, run


@route('/')
@get('/')
def index():
    color = request.query.get('opcao')

    form =  '''
            <h1>Escolha uma opção</h1>
                <a href="/cadastro">Adicionar bicicleta</a>
                <br>
                <a href="/mostrar">Mostrar informações da bicicleta</a>
                <br>
                <a href="/acoes">Ações da bicicleta</a>
                <br>
            '''
    page = f'''
                <h1>Web App</h1>
                <body style="background-color:{color};">
                {form}
                </body>
            '''
    return page


@route('/cadastro')
def cadastro_de_bicicleta():
    form =  '''
            <form action="/process" method="post">
                Qual a cor: <input type="text" name="cor">
                <br>
                Qual o modelo: <input type="text" name="modelo">
                <br>
                Qual o ano: <input type="text" name="ano">
                <br>
                Qual o valor: <input type="text" name="valor">
                <br>
                <input type="submit">
            </form>
            '''
    page = f'<h1>Web App</h1>{form}'
    return page

def salvar_bicicleta(bicicletas):
    with open('bicicletas.txt', 'a', encoding='utf-8') as file:
        for bicicleta in bicicletas:
            linha = f'{bicicleta.cor}|{bicicleta.modelo}|{bicicleta.valor}'
            file.write(linha)

@post('/process')
def index_process():
    bicicletas = []

    cor = request.forms.get('cor')
    modelo = request.forms.get('modelo')
    ano = request.forms.get('ano')
    valor = request.forms.get('valor')
    bicicletas.append(Bicicleta(cor, modelo, ano, valor))
    
    # Salvar em um arquivo txt, ou em um banco de dados sqlite
    salvar_bicicleta(bicicletas)
    message = f'A bicicleta {modelo} {cor}, de {ano} com valor {valor} foi adicionada!'

    return message

@route('/mostrar')
def mostrar_bicicletas():
    pass


run(host='localhost', port=8080)