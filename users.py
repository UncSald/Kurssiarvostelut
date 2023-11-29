from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

# USER CREATION
# CHECK WETHER USERNAME EXISTS OR NOT

def create_user(username, password):
    sql1 = text("SELECT username FROM users WHERE username=:username")
    result = db.session.execute(sql1, {"username":username}).fetchone()
    print(result)
    if result == None:
        print("luodaan käyttäjä")
        hash_value = generate_password_hash(password)
        sql2 = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql2, {"username":username, "password":hash_value})
        db.session.commit()
    else: print("username exists")

# CHECKING WETHER PASSWORD MATCHES SAVED PASSWORD
def check_password(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if user:
        return True
    return False

