from db import db
from sqlalchemy.sql import text



# FUNCTIONS TO ADD DATA TO THE DATABASE

# FUNCTION TO ADD COURSE TO DATABASE
def add_course(course_id, name):
    name = name.upper()
    course_id = course_id.upper()
    sql = text("SELECT course_id FROM courses WHERE course_id = :course_id")
    sql2 = text("INSERT INTO Courses (course_id, name) VALUES (:course_id, :name)")
    course = db.session.execute(sql, {"course_id":course_id}).fetchone()
    
    if not course:
        db.session.execute(sql2, {"course_id":course_id, "name":name})
    
    db.session.commit()
    
# FUNCTION TO ADD REVIEW TO DATABASE
# TABLE REVIEW CONNECTED TO COURSES TABLE
# TABLES TEACHERS, MATERIAL, AND WORKLOAD CONNECTED TO REVIEWS
def add_review(course_id, material, workload, teacher_name, teacher_grade):
    course_id = course_id.upper()
    teacher_name = teacher_name.upper()
    sql = text("INSERT INTO Reviews (course, created) VALUES (:course_id, NOW())")
    db.session.execute(sql, {"course_id":course_id})
    db.session.commit()
    sql1 = text("SELECT MAX(id) FROM Reviews")
    reference = db.session.execute(sql1).fetchone()[0]
    sql2 = text("INSERT INTO Teachers (name, grade, review_id) VALUES (:name, :grade, :review_id)")
    sql3 = text("INSERT INTO Material (grade, review_id) VALUES (:grade, :review_id)")
    sql4 = text("INSERT INTO Workload (grade, review_id) VALUES (:grade, :review_id)")
    db.session.execute(sql2, {"name":teacher_name, "grade":teacher_grade, "review_id":reference})
    db.session.execute(sql3, {"grade":material, "review_id":reference})
    db.session.execute(sql4, {"grade":workload, "review_id":reference})
    db.session.commit()
