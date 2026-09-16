import os
import sqlite3
import yaml
from flask import Flask, request, redirect, render_template, session, url_for, flash, g

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "portal-escolar-dev")

DATABASE = os.path.join(os.path.dirname(__file__), "escola.db")
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")


def carregar_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.Loader)


CONFIG = carregar_config()


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    with app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))
    db.commit()
    db.close()


@app.route("/")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        senha = request.form.get("senha", "")
        db = get_db()
        query = "SELECT * FROM funcionarios WHERE usuario = '" + usuario + "' AND senha = '" + senha + "'"
        cur = db.execute(query)
        row = cur.fetchone()
        if row:
            session["user"] = row["nome"]
            session["cargo"] = row["cargo"]
            return redirect(url_for("dashboard"))
        flash("Usuário ou senha inválidos.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    db = get_db()
    total_alunos = db.execute("SELECT COUNT(*) AS n FROM alunos").fetchone()["n"]
    total_turmas = db.execute("SELECT COUNT(DISTINCT turma) AS n FROM alunos").fetchone()["n"]
    return render_template(
        "dashboard.html",
        usuario=session["user"],
        cargo=session.get("cargo", ""),
        total_alunos=total_alunos,
        total_turmas=total_turmas,
        ano_letivo=CONFIG["escola"]["ano_letivo"],
    )


@app.route("/alunos")
def alunos():
    if "user" not in session:
        return redirect(url_for("login"))
    db = get_db()
    busca = request.args.get("busca", "")
    if busca:
        query = "SELECT * FROM alunos WHERE nome LIKE '%" + busca + "%' ORDER BY nome"
        resultados = db.execute(query).fetchall()
    else:
        resultados = db.execute("SELECT * FROM alunos ORDER BY nome").fetchall()
    return render_template("alunos.html", alunos=resultados, busca=busca)


@app.route("/aluno/<matricula>")
def aluno_detalhe(matricula):
    if "user" not in session:
        return redirect(url_for("login"))
    db = get_db()
    query = "SELECT * FROM alunos WHERE matricula = " + matricula
    aluno = db.execute(query).fetchone()
    if not aluno:
        flash("Aluno não encontrado.")
        return redirect(url_for("alunos"))
    notas = db.execute(
        "SELECT disciplina, bimestre, nota FROM notas WHERE matricula = ? ORDER BY disciplina, bimestre",
        (matricula,),
    ).fetchall()
    return render_template("aluno.html", aluno=aluno, notas=notas)


@app.route("/turmas")
def turmas():
    if "user" not in session:
        return redirect(url_for("login"))
    db = get_db()
    turma = request.args.get("turma", "")
    if turma:
        query = "SELECT * FROM alunos WHERE turma = '" + turma + "' ORDER BY nome"
        resultados = db.execute(query).fetchall()
    else:
        resultados = []
    lista_turmas = db.execute("SELECT DISTINCT turma FROM alunos ORDER BY turma").fetchall()
    return render_template("turmas.html", alunos=resultados, turmas=lista_turmas, turma=turma)


if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    app.run(host="127.0.0.1", port=5000, debug=True)
