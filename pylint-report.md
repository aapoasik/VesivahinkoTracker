# Pylint-tulokset

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:49:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:71:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:81:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:81:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:112:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:118:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:126:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:135:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:135:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:154:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:154:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:174:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:202:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:222:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:231:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:242:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module forum
forum.py:1:0: C0114: Missing module docstring (missing-module-docstring)
forum.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:33:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:55:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:72:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:90:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:90:0: R0913: Too many arguments (7/5) (too-many-arguments)
forum.py:97:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:112:11: W0718: Catching too general exception Exception (broad-exception-caught)
forum.py:116:0: C0116: Missing function or method docstring (missing-function-docstring)
forum.py:120:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:14:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:15:0: C0103: Constant name "report_count" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
```

# Virheiden selitykset ja perustelut

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
```
Suurin osa virheistä on tällaisia virheitä, joissa huomautetaan puuttuvista docstring-kommenteista.
Docstring-kommenttien käyttämättä jättäminen on tietoinen valinta. 


```
app.py:81:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

```
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

...
```
App.py-tiedostossa on kolme tällaista virhettä. Ne huomauttavat siitä, että funktio paluttaa arvon vain tietyillä parametreilla (GET ja POST).
Käytännössä tämä johtuu siitä, että nämä funktiot ovat varautuneet palauttamaan arvon vain tietyillä ```request.method```:in arvoilla.
Tämä ei kuitenkaan ole ongelma, sillä näiden funktioiden dekoraattorit edellyttävät, että ```request.method```:in arvo on jokin niistä, joita funktio osaa käsitellä.


```
app.py:231:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
```
```
...

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

```
Tämä virhe huomauttaa tarpeettomasta else-palikasta. 
Koodin voisi toki kirjoittaa tiiviimmin ilman else:ä, mutta se on päätetty pitää, sillä se tekee rakenteesta selkeämmän.


```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```
```
secret_key = "82beed28c21d7b25c80f67d1a7a0f13d"
```
Tällaisia virheitä löytyy config.py- ja seed.py-tiedostoista. Ne huomauttavat siitä, että vakioksi tulkittu muuttuja on kirjoitettu pienillä kirjaimilla.
Muuttuja on tietoisesti päätetty kirjoittaa pienillä kirjaimilla, sillä se sopii paremmin sovelluksen koodin tyyliin.


```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```
```
def execute(sql, params=[]):
    con = get_connection()
    with con:
        result = con.execute(sql, params)
    g.last_insert_id = result.lastrowid
    con.close()

...

def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
```
Tämä virhe huomauttaa oletusarvosta, joka on jaettu kahden funktion välillä. Tämä voisi aiheuttaa ongelmia, jos funktiot muuttaisivat tätä arvoa.
Funktiot eivät kuitenkaan muuta tätä listaa, joten ei ole vaaraa, että tämä oletusarvo aiheuttaisi ongelmia.


```
forum.py:90:0: R0913: Too many arguments (7/5) (too-many-arguments)
```
```
def add_report(title, content, sent_at, image, user_id, location_id, alttext):
    sql = "INSERT INTO Reports (title, content, sent_at, image, user_id, location_id, alttext) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, content, sent_at, image, user_id, location_id, alttext])
    report_id = db.last_insert_id()
    return report_id
```
Tämä virhe huomauttaa funktiokutsusta, jossa on liian monta argumenttia. Kaikki argumentit ovat oleellisia, ja kyseessä on yksittäistapaus.
Siispä funktion on annettu pysyä sellaisenaan. 


```
forum.py:112:11: W0718: Catching too general exception Exception (broad-exception-caught)
```
```
...
    insert_sql = "INSERT INTO Reactions (report_id, user_id, emoji_id) VALUES (?, ?, ?)"
    try:
        db.execute(insert_sql, [report_id, user_id, emoji_id])
        reaction_id = db.last_insert_id()
        return reaction_id
    except Exception as e:
        print(f"Failed to add reaction, user may have already reacted: {e}")
        return None
```
Tämä virhe huomauttaa ```except```-palikasta, joka vastaanottaa minkä tahansa virheen. 
Haluamme varmuuden vuoksi varmistaa, että mitään ei tapahdu, jos jokin menee pieleen yllä olevassa kyselyssä.
