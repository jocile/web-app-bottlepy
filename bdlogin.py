import hashlib
import sqlite3

from bottle import Bottle, redirect, request, response, run, template

app = Bottle()
DB_FILE = "tarefas.db"
COOKIE_SECRET = (
    "uma_chave_muito_secreta_e_longa_123456"  # Usada para criptografar o cookie
)


def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # Tabela de Tarefas vinculada a um usuario_id
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            titulo TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente'
        )
    """)
    # Nova tabela de Usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# Função auxiliar para criptografar a senha antes de salvar/comparar
def hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# Função auxiliar para pegar o usuário logado via Cookie
def get_current_user():
    return request.get_cookie("usuario_logado", secret=COOKIE_SECRET)


# --- ROTAS DE AUTENTICAÇÃO ---


@app.route("/cadastro")
def form_cadastro():
    return template("cadastro", erro=None)


@app.route("/cadastro", method="POST")
def fazer_cadastro():
    username = request.forms.get("username").strip()
    password = request.forms.get("password")

    if not username or not password:
        return template("cadastro", erro="Preencha todos os campos.")

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (username, password) VALUES (?, ?)",
            (username, hash_password(password)),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return template("cadastro", erro="Este nome de usuário já existe.")
    finally:
        db.close()

    return redirect("/login")


@app.route("/login")
def form_login():
    return template("login", erro=None)


@app.route("/login", method="POST")
def fazer_login():
    username = request.forms.get("username")
    password = request.forms.get("password")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND password = ?",
        (username, hash_password(password)),
    )
    usuario = cursor.fetchone()
    db.close()

    if usuario:
        # Salva o ID do usuário no cookie criptografado (expira em 1 hora)
        response.set_cookie(
            "usuario_logado",
            str(usuario["id"]),
            secret=COOKIE_SECRET,
            max_age=3600,
            path="/",
        )
        return redirect("/")

    return template("login", erro="Usuário ou senha incorretos.")


@app.route("/logout")
def fazer_logout():
    response.delete_cookie("usuario_logado", path="/")
    return redirect("/login")


# --- ROTAS DO CRUD PROTEGIDAS ---


@app.route("/")
def index():
    usuario_id = get_current_user()
    if not usuario_id:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()
    # Mostra apenas as tarefas do usuário logado
    cursor.execute("SELECT * FROM tarefas WHERE usuario_id = ?", (usuario_id,))
    lista_tarefas = cursor.fetchall()
    db.close()
    return template("tarefas", tarefas=lista_tarefas)


@app.route("/nova", method="POST")
def nova_tarefa():
    usuario_id = get_current_user()
    if not usuario_id:
        return redirect("/login")

    titulo = request.forms.get("titulo")
    if titulo:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO tarefas (usuario_id, titulo) VALUES (?, ?)",
            (usuario_id, titulo),
        )
        db.commit()
        db.close()
    return redirect("/")


@app.route("/editar/<id:int>")
def form_editar(id):
    usuario_id = get_current_user()
    if not usuario_id:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()
    # Garante que o usuário só edite suas próprias tarefas
    cursor.execute(
        "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?", (id, usuario_id)
    )
    tarefa = cursor.fetchone()
    db.close()
    if tarefa:
        return template("tarefas-editar", tarefa=tarefa)
    return "Tarefa não encontrada ou acesso negado."


@app.route("/editar/<id:int>", method="POST")
def salvar_edicao(id):
    usuario_id = get_current_user()
    if not usuario_id:
        return redirect("/login")

    titulo = request.forms.get("titulo")
    status = request.forms.get("status")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE tarefas SET titulo = ?, status = ? WHERE id = ? AND usuario_id = ?",
        (titulo, status, id, usuario_id),
    )
    db.commit()
    db.close()
    return redirect("/")


@app.route("/deletar/<id:int>")
def deletar_tarefa(id):
    usuario_id = get_current_user()
    if not usuario_id:
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM tarefas WHERE id = ? AND usuario_id = ?", (id, usuario_id)
    )
    db.commit()
    db.close()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    run(app, host="localhost", port=8080, debug=True, reloader=True)
