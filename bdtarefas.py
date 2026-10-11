import os
import sqlite3

from bottle import Bottle, redirect, request, run, template

app = Bottle()
DB_FILE = "tarefas.db"


# Função para conectar ao banco de dados
def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = (
        sqlite3.Row
    )  # Permite acessar colunas pelo nome (ex: row['nome'])
    return conn


# Cria a tabela inicial caso não exista
def init_db():
    if not os.path.exists(DB_FILE):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                status TEXT DEFAULT 'Pendente'
            )
        """)
        # Inserir alguns dados de exemplo
        cursor.execute("INSERT INTO tarefas (titulo) VALUES ('Aprender Bottle Python')")
        cursor.execute("INSERT INTO tarefas (titulo) VALUES ('Configurar SQLite')")
        conn.commit()
        conn.close()


# --- ROTAS DO CRUD ---


# 1. LER (Read) - Listar todas as tarefas
@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tarefas")
    lista_tarefas = cursor.fetchall()
    db.close()
    return template("tarefas", tarefas=lista_tarefas)


# 2. CRIAR (Create) - Adicionar nova tarefa
@app.route("/nova", method="POST")
def nova_tarefa():
    titulo = request.forms.get("titulo")
    if titulo:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO tarefas (titulo) VALUES (?)", (titulo,))
        db.commit()
        db.close()
    return redirect("/")


# 3. ATUALIZAR (Update) - Formulário de edição
@app.route("/editar/<id:int>")
def form_editar(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id,))
    tarefa = cursor.fetchone()
    db.close()
    if tarefa:
        return template("tarefas-editar", tarefa=tarefa)
    return "Tarefa não encontrada."


# 3. ATUALIZAR (Update) - Salvar alterações
@app.route("/editar/<id:int>", method="POST")
def salvar_edicao(id):
    titulo = request.forms.get("titulo")
    status = request.forms.get("status")

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE tarefas SET titulo = ?, status = ? WHERE id = ?", (titulo, status, id)
    )
    db.commit()
    db.close()
    return redirect("/")


# 4. DELETAR (Delete) - Excluir tarefa
@app.route("/deletar/<id:int>")
def deletar_tarefa(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (id,))
    db.commit()
    db.close()
    return redirect("/")


if __name__ == "__main__":
    init_db()
    run(app, host="localhost", port=8080, debug=True, reloader=True)
