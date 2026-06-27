from flask import Flask
from flask import abort, flash, g, make_response, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config, forum, db, re, users
import datetime, markupsafe, math, secrets, sqlite3, time

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

@app.template_filter()
def line_breaks(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(((time.time() - g.start_time) * 1000), 3)
    print("elapsed time:", elapsed_time, "ms")
    return response

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    report_count = forum.report_count()
    page_count = math.ceil(report_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    reports = forum.get_reports(page, page_size)
    try:
        user_id = session["user_id"]
        locations = forum.get_locations()
        username = users.get_user(user_id)
        return render_template("index.html", reports=reports, page=page, page_count=page_count, username=username, locations=locations)
    except KeyError:
        return render_template("index.html", reports=reports, page=page, page_count=page_count)

@app.route("/image/<int:report_id>")
def show_image(report_id):
    image = forum.get_image(report_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if len(username) > 30 or len(username) < 3:
            flash("Käyttäjänimen tulee olla 3-30 merkkiä!")
            return redirect("/register")

        if username == "":
            flash("Syötä käyttäjänimi!")
            return redirect("/register")

        if password1 != password2:
            flash("Salasanat eivät täsmää!")
            return redirect("/register")

        if password1 == "":
            flash("Syötä salasana!")
            return redirect("/register")

        try:
            users.create_user(username, password1)
            flash("Käyttäjätili luotu!")
            return redirect("/login")

        except sqlite3.IntegrityError:
            flash("Tämä käyttäjänimi on jo käytössä!")
            return redirect("/register")

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
    location_id = request.form["location_id"]
    sent_at = date_time
    alttext = request.form["alttext"]

    file = request.files["image"]
    if file and not file.filename.endswith(".jpg"):
        flash("Kuva ei kelpaa; lähetä JPEG-tiedosto!")
        return redirect("/")

    image = file.read()
    if len(image) > 1000 * 1024:
        flash("Kuva on liian suuri; maksimikoko on 1 Mt!")
        return redirect("/")

    if not title or len(title) > 60 or len(content) > 2000:
        abort(403)

    report_id = forum.add_report(title, content, sent_at, image, user_id, location_id, alttext)
    return redirect("/report/" + str(report_id))

@app.route("/new_reaction", methods=["POST"])
def new_reaction():
    check_csrf()
    require_login()

    report_id = request.form["report_id"]
    if "emoji" not in request.form:
        return redirect("/report/" + str(report_id))
    emoji = request.form["emoji"]
    if emoji not in ["1", "2", "3", "4", "5"]:
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
        return render_template("login.html", next_page=request.referrer)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

    user_id = users.check_login(username, password)
    if user_id:
        session["user_id"] = user_id
        session["csrf_token"] = secrets.token_hex(16)
        if re.findall("register$", next_page):
            return redirect("/")
        return redirect(next_page)
    else:
        flash("Väärä käyttäjänimen ja salasanan yhdistelmä!")
        return render_template("login.html", next_page=next_page)

@app.route("/logout")
def logout():
    try:
        del session["user_id"]
    except KeyError:
        pass
    return redirect("/")
