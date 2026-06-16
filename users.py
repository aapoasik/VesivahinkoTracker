from werkzeug.security import check_password_hash, generate_password_hash
import db

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = "SELECT id, password_hash FROM Users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            print(user_id, password_hash)
            return user_id
    return None

def get_user(user_id):
    sql = "SELECT username FROM Users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_reports(user_id):
    sql = """SELECT r.id report_id,
                    r.title,
                    r.sent_at
             FROM Reports r
             WHERE r.user_id = ?
             ORDER BY r.sent_at DESC"""
    return db.query(sql, [user_id])
