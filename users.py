from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


# USER CREATION
# CHECK WETHER USERNAME EXISTS OR NOT
def create_user(username, password):
    sql1 = text("SELECT username FROM users WHERE username=:username")
    result = db.session.execute(sql1, {"username":username}).fetchone()
    if result is None:
        hash_value = generate_password_hash(password)
        sql2 = text("""INSERT INTO users (username, password, rights)
                        VALUES (:username, :password, False)""")
        db.session.execute(sql2, {"username":username, "password":hash_value})
        db.session.commit()
    return bool(result)



# CHECKING WETHER PASSWORD MATCHES SAVED PASSWORD
def check_password(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user:
        pw_hash = user.password
        return bool(check_password_hash(pw_hash, password))
    return False



# CHECK IF USER HAS ADMIN RIGHTS
def is_admin(username):
    sql = text("SELECT rights FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username}).fetchone()[0]
    return result
