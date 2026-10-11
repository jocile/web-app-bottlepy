import sqlite3

from bottle import Bottle, request, run

app = Bottle()


def get_db():
    conn = sqlite3.connect("tarefas.db")
    conn.row_factory = sqlite3.Row  # Permite acessar as colunas pelo nome
    return conn


@app.route("/usuarios")
def listar_usuarios():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    db.close()

    # Exemplo simples de retorno
    return {"usuarios": [dict(row) for row in usuarios]}


@app.route("/usuarios", method="POST")
def criar_usuario():
    nome = request.forms.get("nome")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO usuarios (nome) VALUES (?)", (nome,))
    db.commit()
    db.close()
    return "Usuário criado com sucesso!"


if __name__ == "__main__":
    run(app, host="localhost", port=8080)
