from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config, forum, db, users
import sqlite3

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    reports = forum.get_reports()
    return render_template("index.html", reports=reports)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return "VIRHE: salasanat eivät täsmää!"

        try:
            users.create_user(username, password1)
            return "Käyttäjätili luotu!"
        except sqlite3.IntegrityError:
            return "VIRHE: käyttäjänimi on jo käytössä!"

@app.route("/report/<int:report_id>")
def show_report(report_id):
    report = forum.get_report(report_id)
    return render_template("report.html", report=report)

@app.route("/edit/<int:report_id>", methods=["GET", "POST"])
def edit_report(report_id):
    report = forum.get_report(report_id)

    if request.method == "GET":
        return render_template("edit.html", report=report)

    if request.method == "POST":
        content = request.form["content"]
        forum.update_report(report["id"], content)
        return redirect("/report/" + str(report["report_id"]))

@app.route("/new_report", methods=["POST"])
def new_report():
    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]

    report_id = forum.add_report(title, content, user_id)
    return redirect("/report/" + str(report_id))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        return redirect("/")
    else:
        return "VIRHE: väärä käyttäjänimen ja salasanan yhdistelmä!"

@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")
