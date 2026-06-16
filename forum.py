import db

def report_count():
    sql = "SELECT COUNT(*) FROM Reports"
    return db.query(sql)[0][0]

def search(query):
    sql = """SELECT r.title report_title, r.id report_id,
                    r.sent_at, u.username, u.id user_id
             FROM Reports r, Users u
             WHERE u.id = r.user_id AND
                   r.content LIKE ?
             ORDER BY r.sent_at DESC"""
    return db.query(sql, ["%" + query + "%"])

def get_reports(page, page_size):
    sql = """SELECT r.id, r.title, u.username, u.id user_id,
                    COUNT(r.id) total, MAX(r.sent_at) last,
             SUM(CASE WHEN e.emoji = '🌚' THEN 1 ELSE 0 END) AS moon_count,
             SUM(CASE WHEN e.emoji = '🐳' THEN 1 ELSE 0 END) AS whale_count,
             SUM(CASE WHEN e.emoji = '🗿' THEN 1 ELSE 0 END) AS moai_count,
             SUM(CASE WHEN e.emoji = '😭' THEN 1 ELSE 0 END) AS crying_count,
             SUM(CASE WHEN e.emoji = '🫠' THEN 1 ELSE 0 END) AS melting_count
             FROM Reports r
             LEFT JOIN Users u ON r.user_id = u.id
             LEFT JOIN Reactions e on r.id = e.report_id
             GROUP BY r.id, u.username, u.id
             ORDER BY r.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

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

def update_report(report_id, content):
    sql = "UPDATE Reports SET content = ? WHERE id = ?"
    db.execute(sql, [content, report_id])

def delete_report(report_id):
    sql_reactions = "DELETE FROM Reactions WHERE report_id = ?"
    db.execute(sql_reactions, [report_id])
    sql_report = "DELETE FROM Reports WHERE id = ?"
    db.execute(sql_report, [report_id])
