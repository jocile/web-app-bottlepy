from bicicletario import Bicicleta
from bottle import get, post, request, route, run


def carregar_bicicletas():
    """Carrega as bicicletas de um arquivo TXT"""
    bicicletas = []
    try:
        with open('bicicletas.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split('|')
                if len(partes) >= 4:
                    valor_float = float(partes[3])
                    bicicletas.append(Bicicleta(partes[0], partes[1], partes[2], valor_float))
    except FileNotFoundError:
        pass
    return bicicletas


def salvar_bicicletas(bicicletas):
    """Salva as bicicletas em um arquivo TXT"""
    with open('bicicletas.txt', 'w', encoding='utf-8') as f:
        for bicicleta in bicicletas:
            linha = f"{bicicleta.cor}|{bicicleta.modelo}|{bicicleta.ano}|{bicicleta.valor}\n"
            f.write(linha)


@route("/")
@get("/")
def index():
    color = request.query.get("opcao")

    form = '''
                <h1>Escolha uma opcao</h1>
                <a href="/cadastro">Adicionar bicicleta</a>
                <br>
                    <a href="/mostrar">Mostrar informacoes da bicicleta</a>
                <br>
                    <a href="/acoes">Acoes da bicicleta</a>
                <br>
            '''
    page = f'''
                <h1>Web App</h1>
                <body style="background-color:{color};">
                {form}
                </body>
            '''
    return page


@route("/cadastro")
def cadastro_de_bicicleta():
    #bicicletas = carregar_bicicletas()
    
    form = '''
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
    page = f"<h1>Web App</h1>{form}"
    return page


@post("/process")
def index_process():
    cor = request.forms.get("cor")
    modelo = request.forms.get("modelo")
    ano = request.forms.get("ano")
    valor = float(request.forms.get("valor"))
    
    bicicleta = Bicicleta(cor, modelo, ano, valor)
    
    bicicletas = carregar_bicicletas()
    bicicletas.append(bicicleta)
    salvar_bicicletas(bicicletas)
    
    message = f"A bicicleta {modelo} {cor}, de {ano} com valor {valor} foi adicionada!"

    return message


@route("/mostrar")
def mostrar_bicicletas():
    bicicletas = carregar_bicicletas()

    form = '''
        <h1>Listagem de Bicicletas</h1>
        <ul>
        '''

    for i, bicicleta in enumerate(bicicletas):
        form += f'<li><strong>Bicicleta {i + 1}</strong>: Cor: {bicicleta.cor}, Modelo: {bicicleta.modelo}, Ano: {bicicleta.ano}, Valor: R${bicicleta.valor:.2f}</li>'

    if not bicicletas:
        form += "<p>Nenhuma bicicleta cadastrada.</p>"

    form += "</ul>"
    page = f"<h1>Web App</h1>{form}"
    return page


@route("/acoes")
def acoes_bicicletas():
    bicicletas = []

    form = '''
        <h1>Ações das Bicicletas</h1>
        <ul>
        '''

    for i, bicicleta in enumerate(bicicletas):
        form += f'''<li><strong>Bicicleta {i + 1}</strong>: Cor: {bicicleta.cor}, Modelo: {bicicleta.modelo}, Ano: {bicicleta.ano}, Valor: R${bicicleta.valor:.2f}<br>
            <button onclick=alert("Buzinar!");>Buzinar</button> 
            <button onclick=alert("Correr!");>Correr</button> 
            <button onclick=alert("Parar!");>Parar</button></li>
        '''

    form += "</ul>"
    page = f"<h1>Web App</h1>{form}"
    return page


run(host="localhost", port=8080)
