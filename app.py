from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config, forum, db, users
import sqlite3, datetime, secrets

app = Flask(__name__)
app.secret_key = config.secret_key

#fetch and format dates and times for timestamps
date_time_unformatted = datetime.datetime.now()
date_time = date_time_unformatted.strftime("%d.%m.%Y klo %H:%M")

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    reports = forum.get_reports()
    try:
        user_id = session["user_id"]
        username = users.get_username(user_id)
        return render_template("index.html", reports=reports, username=username)
    except KeyError:
        return render_template("index.html", reports=reports)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if username == "":
            return render_template("registered.html", result="Käyttäjänimi ei voi olla tyhjä!", success=False)
        if password1 != password2:
            return render_template("registered.html", result="Salasanat eivät täsmää!", success=False)
        if password1 == "":
            return render_template("registered.html", result="Salasana ei voi olla tyhjä!", success=False)
        try:
            users.create_user(username, password1)
            return render_template("registered.html", result="Käyttäjätili luotu!", success=True)
        except sqlite3.IntegrityError:
            return render_template("registered.html", result="Tämä käyttäjänimi on jo käytössä!", success=False)

@app.route("/search")
def search():
    query = request.args.get("query")
    results = forum.search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    reports = users.get_reports(user_id)
    return render_template("profile.html", user=user, reports=reports)

@app.route("/report/<int:report_id>")
def show_report(report_id):
    try:
        report = forum.get_report(report_id)
    except IndexError:
        abort(404)
    reactions = forum.get_reactions(report_id)
    return render_template("report.html", report=report, reactions=reactions)

@app.route("/edit/<int:report_id>", methods=["GET", "POST"])
def edit_report(report_id):
    require_login()

    report = forum.get_report(report_id)
    if report["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", report=report)

    if request.method == "POST":
        check_csrf()
        content = request.form["content"]
        if len(content) > 2000:
            abort(403)
        forum.update_report(report["id"], content)
        return redirect("/report/" + str(report_id))

@app.route("/delete/<int:report_id>", methods=["GET", "POST"])
def delete(report_id):
    require_login()

    report = forum.get_report(report_id)
    if report["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete.html", report=report)

    if request.method == "POST":
        check_csrf()

        if "continue" in request.form:
            forum.delete_report(report["id"])
            return redirect("/")
        if "cancel" in request.form:
            return redirect("/report/" + str(report_id))

@app.route("/new_report", methods=["POST"])
def new_report():
    check_csrf()
    require_login()

    title = request.form["title"]
    content = request.form["content"]
    user_id = session["user_id"]
    sent_at = date_time
    if not title or len(title) > 60 or len(content) > 2000:
        abort(403)

    report_id = forum.add_report(title, content, sent_at, user_id)
    return redirect("/report/" + str(report_id))

@app.route("/new_reaction", methods=["POST"])
def new_reaction():
    check_csrf()
    require_login()

    report_id = request.form["report_id"]
    if "emoji" not in request.form:
        return redirect("/report/" + str(report_id))
    emoji = request.form["emoji"]
    if emoji not in ["🌚", "🐳", "🗿", "😭", "🫠"]:
        abort(403)
    try:
        user_id = session["user_id"]
        forum.add_reaction(emoji, report_id, user_id)
        return redirect("/report/" + str(report_id))
    except sqlite3.IntegrityError:
        abort(403)
    except KeyError:
        return redirect("/report/" + str(report_id))
date_time_unformatted = datetime.datetime.now()
date_time = date_time_unformatted.strftime("%d.%m.%Y klo %H:%M")

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
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        return render_template("loggedin.html", result="Väärä käyttäjänimen ja salasanan yhdistelmä!")

@app.route("/logout")
def logout():
    try:
        del session["user_id"]
    except KeyError:
        pass
    return redirect("/")
