from db import db
from sqlalchemy.sql import text

def add_course(name, course_id):
    sql = text("INSERT INTO Courses (name, course_id) VALUES (:name, :course_id)")
    db.session.execute(sql, {"name":name, "course_id":course_id})
    db.session.commit()

def get_courses():
    courses = db.session.execute(text("SELECT * FROM Courses")).fetchall()
    return courses