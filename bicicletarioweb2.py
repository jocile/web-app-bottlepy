from bicicletario import Bicicleta
from bottle import get, post, request, route, run


def carregar_bicicletas(nome_arquivo="bicicletas.txt"):
    """Carrega as bicicletas de um arquivo TXT"""
    bicicletas = []
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            for linha in f:
                partes = linha.strip().split('|')
                if len(partes) >= 4:
                    valor_float = float(partes[3])
                    bicicletas.append(Bicicleta(partes[0], partes[1], partes[2], valor_float))
    except FileNotFoundError:
        pass
    return bicicletas


def salvar_bicicletas(bicicletas, nome_arquivo="bicicletas.txt"):
    """Salva as bicicletas em um arquivo TXT"""
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for bicicleta in bicicletas:
            linha = f"{bicicleta.cor}|{bicicleta.modelo}|{bicicleta.ano}|{bicicleta.valor}\n"
            f.write(linha)


def vender_bicicleta(bicicletas, bicicletas_vendidas, numero):
    """Move uma bicicleta do estoque para a lista de bicicletas vendidas."""
    if not 1 <= numero <= len(bicicletas):
        raise ValueError("Número de bicicleta inválido.")

    bicicleta = bicicletas.pop(numero - 1)
    bicicletas_vendidas.append(bicicleta)
    return bicicleta


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
                    <a href="/vender">Vender uma bicicleta</a>
                <br>
                    <a href="/vendidas">Mostrar bicicletas vendidas</a>
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


@route("/vender")
def pagina_venda():
    bicicletas = carregar_bicicletas()
    if not bicicletas:
        return "<h1>Vender bicicleta</h1><p>Nenhuma bicicleta disponível para venda.</p>"

    opcoes = "".join(
        f'<option value="{i}">{bicicleta}</option>'
        for i, bicicleta in enumerate(bicicletas, start=1)
    )
    return f'''
        <h1>Vender bicicleta</h1>
        <form action="/processar-venda" method="post">
            <label for="numero">Escolha a bicicleta:</label>
            <select id="numero" name="numero">{opcoes}</select>
            <input type="submit" value="Vender">
        </form>
    '''


@post("/processar-venda")
def processar_venda():
    bicicletas = carregar_bicicletas()
    bicicletas_vendidas = carregar_bicicletas("bicicletas_vendidas.txt")
    try:
        numero = int(request.forms.get("numero"))
    except (TypeError, ValueError):
        return "<p>Número de bicicleta inválido.</p>"

    try:
        bicicleta = vender_bicicleta(bicicletas, bicicletas_vendidas, numero)
    except ValueError as erro:
        return f"<p>{erro}</p>"

    salvar_bicicletas(bicicletas)
    salvar_bicicletas(bicicletas_vendidas, "bicicletas_vendidas.txt")
    return f"<p>Bicicleta vendida: {bicicleta}</p>"


@route("/vendidas")
def mostrar_bicicletas_vendidas():
    bicicletas = carregar_bicicletas("bicicletas_vendidas.txt")
    if not bicicletas:
        return "<h1>Bicicletas vendidas</h1><p>Nenhuma bicicleta vendida.</p>"

    itens = "".join(f"<li>{bicicleta}</li>" for bicicleta in bicicletas)
    return f"<h1>Bicicletas vendidas</h1><ul>{itens}</ul>"


@route("/acoes")
def acoes_bicicletas():
    bicicletas = carregar_bicicletas()

    form = '''
        <h1>Ações das Bicicletas</h1>
        <ul>
        '''

    for i, bicicleta in enumerate(bicicletas, start=1):
        form += f'''<li><strong>Bicicleta {i}</strong>: Cor: {bicicleta.cor}, Modelo: {bicicleta.modelo}, Ano: {bicicleta.ano}, Valor: R${bicicleta.valor:.2f}<br>
            <button onclick=alert("Buzinar!");>Buzinar</button> 
            <button onclick=alert("Correr!");>Correr</button> 
            <button onclick=alert("Parar!");>Parar</button>
            <form action="/processar-venda" method="post" style="display:inline;">
                <input type="hidden" name="numero" value="{i}">
                <button type="submit">Vender</button>
            </form></li>
        '''

    if not bicicletas:
        form += "<li>Nenhuma bicicleta cadastrada.</li>"

    form += "</ul>"
    page = f"<h1>Web App</h1>{form}"
    return page


run(host="localhost", port=8081)
