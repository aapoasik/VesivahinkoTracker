import db

def report_count():
    sql = "SELECT COUNT(*) FROM Reports"
    return db.query(sql)[0][0]

def search(query):
    sql = """SELECT r.title report_title,
                    r.id report_id,
                    r.sent_at,
                    u.username,
                    l.value
             FROM Reports r, Users u, Locations l
             WHERE u.id = r.user_id AND l.id = r.location_id
             AND (r.content LIKE ?
             OR r.title LIKE ?
             OR u.username LIKE ?
             OR l.value LIKE ?
             OR r.alttext LIKE ?)
             ORDER BY r.sent_at DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%", "%" + query + "%", "%" + query + "%", "%" + query + "%"])

def get_locations():
    sql = "SELECT l.value, l.id FROM Locations l ORDER BY l.value"
    return db.query(sql)

def get_reports(page, page_size):
    sql = """SELECT r.id,
                    r.title,
                    u.username,
                    l.value,
                    r.location_id,
                    u.id user_id,
                    r.sent_at last_sent,
                    r.moon_count,
                    r.whale_count,
                    r.moai_count,
                    r.crying_count,
                    r.melting_count
             FROM Reports r
             JOIN Users u ON r.user_id = u.id
             JOIN Locations l ON r.location_id = l.id
             ORDER BY r.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_report(report_id):
    sql = """SELECT r.id,
                    r.content,
                    r.location_id,
                    r.sent_at,
                    r.title,
                    r.image IS NOT NULL has_image,
                    r.alttext,
                    r.user_id,
                    u.username,
                    l.value
             FROM Reports r
             JOIN Locations l ON r.location_id = l.id
             JOIN Users u ON r.user_id = u.id
             WHERE r.id = ?"""
    return db.query(sql, [report_id])[0]

def get_reactions(report_id):
    sql = """SELECT e.emoji_char emoji,
                    COUNT(a.user_id) reaction_count,
                    GROUP_CONCAT(a.user_id) user_ids
             FROM Reactions a
             JOIN Emojis e ON a.emoji_id = e.id
             WHERE a.report_id = ?
             GROUP BY e.emoji_char"""
    try:
        return db.query(sql, [report_id])
    except IndexError:
        return None

def get_image(report_id):
    sql = "SELECT image FROM Reports WHERE id = ?"
    result = db.query(sql, [report_id])
    return result[0][0] if result else None

def add_report(title, content, sent_at, image, user_id, location_id, alttext):
    sql = "INSERT INTO Reports (title, content, sent_at, image, user_id, location_id, alttext) VALUES (?, ?, ?, ?, ?, ?, ?)"
    db.execute(sql, [title, content, sent_at, image, user_id, location_id, alttext])
    report_id = db.last_insert_id()
    return report_id

def add_reaction(emoji, report_id, user_id):
    get_id_sql = "SELECT id FROM Emojis WHERE id = ?"
    try:
        result = db.query(get_id_sql, [emoji])
        if not result:
            raise ValueError(f"Invalid emoji: {emoji}")
        emoji_id = result[0]['id']
    except IndexError:
        raise ValueError(f"Invalid emoji provided: {emoji}")

    insert_sql = "INSERT INTO Reactions (report_id, user_id, emoji_id) VALUES (?, ?, ?)"
    try:
        db.execute(insert_sql, [report_id, user_id, emoji_id])
        reaction_id = db.last_insert_id()
        return reaction_id
    except Exception as e:
        print(f"Failed to add reaction, user may have already reacted: {e}")
        return None

def update_report(report_id, content):
    sql = "UPDATE Reports SET content = ? WHERE id = ?"
    db.execute(sql, [content, report_id])

def delete_report(report_id):
    sql_reactions = "DELETE FROM Reactions WHERE report_id = ?"
    db.execute(sql_reactions, [report_id])
    sql_report = "DELETE FROM Reports WHERE id = ?"
    db.execute(sql_report, [report_id])
