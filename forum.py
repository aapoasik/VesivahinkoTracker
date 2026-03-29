import db

def get_reports():
    sql = """SELECT r.id, r.title, COUNT(r.id) total, MAX(r.sent_at) last
             FROM Reports r
             GROUP BY r.id
             ORDER BY r.id DESC"""
    return db.query(sql)

def get_report(report_id):
    sql = "SELECT id, title FROM Reports WHERE id = ?"
    return db.query(sql, [report_id])[0]

def add_report(title, content, user_id):
    sql = "INSERT INTO Reports (title, user_id) VALUES (?, ?)"
    db.execute(sql, [title, user_id])
    report_id = db.last_insert_id()
    return report_id
