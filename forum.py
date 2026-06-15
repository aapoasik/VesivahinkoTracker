import db

def get_reports():
    sql = """SELECT r.id, r.title, u.username, COUNT(r.id) total, MAX(r.sent_at) last
             FROM Reports r
             LEFT JOIN Users u ON r.user_id = u.id
             GROUP BY r.id, u.username
             ORDER BY r.id DESC"""
    return db.query(sql)

def get_report(report_id):
    sql = """SELECT r.id, r.content, r.sent_at, r.title, r.user_id, u.username
             FROM Reports r
             JOIN Users u ON r.user_id = u.id
             WHERE r.id = ?"""
    return db.query(sql, [report_id])[0]

def get_reactions(report_id):
    sql = """SELECT emoji, COUNT(user_id) AS reaction_count,
             GROUP_CONCAT(user_id) AS user_ids
             FROM Reactions WHERE report_id = ?
             GROUP BY emoji"""
    try:
        return db.query(sql, [report_id])
    except IndexError:
        return None

def add_report(title, content, sent_at, user_id):
    sql = "INSERT INTO Reports (title, content, sent_at, user_id) VALUES (?, ?, ?, ?)"
    db.execute(sql, [title, content, sent_at, user_id])
    report_id = db.last_insert_id()
    return report_id

def add_reaction(emoji, report_id, user_id):
    sql = "INSERT INTO Reactions (emoji, report_id, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [emoji, report_id, user_id])
    reaction_id = db.last_insert_id()
    return reaction_id
