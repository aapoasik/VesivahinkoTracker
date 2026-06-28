import random
import sqlite3

db = sqlite3.connect("database.db")

print("Aloitetaan tietokannan tyhjentäminen")

db.execute("DELETE FROM Users")
db.execute("DELETE FROM Reports")
db.execute("DELETE FROM Reactions")

print("Tietokanta tyhjennetty, aloitetaan testidatan populointi")

user_count = 10**5
report_count = 10**6

for i in range(1, user_count + 1):
    if i % 1000 == 0:
        print(f"Populoidaan käyttäjiä ({i}/{user_count})")
    db.execute("INSERT INTO Users (username) VALUES (?)",
               ["user" + str(i)])

print("Käyttäjät populoitu")

for i in range(1, report_count + 1):
    if i % 1000 == 0:
        print(f"Populoidaan raportteja ({i}/{report_count})")
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO Reports (title, content, sent_at, user_id, location_id) VALUES (?, ?, ?, ?, ?)",
               ["thread" + str(i), "content" + str(i), "joskus", user_id, 1])

print("Raportit populoitu")

for i in range(1, report_count):
    if i % 1000 == 0:
        print(f"Populoidaan hajautettuja reaktioita ({i}/{report_count})")
    user_id = random.randint(1, user_count)
    report_id = i
    emoji_id = random.randint(1, 5)
    db.execute("""INSERT INTO Reactions (emoji_id, user_id, report_id)
                  VALUES (?, ?, ?)""",
               [emoji_id, user_id, report_id])

print("Hajautetu reaktiot populoitu")

for i in range(1, user_count + 1):
    if i % 1000 == 0:
        print(f"Populoidaan kohdistettuja reaktioita ({i}/{user_count})")

    user_id = i
    emoji_id = random.randint(1, 5)
    db.execute("""INSERT INTO Reactions (emoji_id, user_id, report_id)
                  VALUES (?, ?, ?)""",
               [emoji_id, user_id, report_count])

print("Kohdistetut reaktiot populoitu")
print("Testidatan populointi valmis")

db.commit()
db.close()
