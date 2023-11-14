from db import db
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash


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

def check_password(username, password):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()    
    if not user:
        return 0
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return 2
        else:
            return 1

def add_course(name, course_id):
    sql = text("INSERT INTO Courses (name, course_id) VALUES (:name, :course_id)")
    db.session.execute(sql, {"name":name, "course_id":course_id})
    db.session.commit()

def get_courses():
    sql = text("SELECT * FROM Courses")
    result = db.session.execute(sql)
    courses = result.fetchall()
    return courses
