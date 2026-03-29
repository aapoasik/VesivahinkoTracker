from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config, forum, db
import sqlite3

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    reports = forum.get_reports()
    return render_template("index.html", reports=reports)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät täsmää!"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: Tämä käyttäjänimi on jo käytössä!"

    return "Tunnus luotu"

@app.route("/edit/<int:report_id>", methods=["GET", "POST"])
def edit_report(report_id):
    report = forum.get_report(report_id)

    if request.method == "GET":
        return render_template("edit.html", report=report)

    if request.method == "POST":
        content = request.form["content"]
        forum.update_report(report["id"], content)
        return redirect("/report/" + str(report["report_id"]))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    sql = "SELECT password_hash FROM users WHERE username = ?"
    try:
        password_hash = db.query(sql, [username])[0][0]
    except IndexError:
        return "VIRHE: väärä käyttäjänimen ja salasanan yhdistelmä!"
    if check_password_hash(password_hash, password):
        session["username"] = username
        return redirect("/")
    else:
        return "VIRHE: väärä käyttäjänimen ja salasanan yhdistelmä!"

@app.route("/new_report", methods=["POST"])
def new_report():
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]

    report_id = forum.add_report(title, content, user_id)
    return redirect("/report/" + str(report_id))

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
