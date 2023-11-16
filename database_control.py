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
    if not user:
        return 0
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            return 2
        else:
            return 1


# MODULES TO ADD DATA TO THE DATABASE

# MODULE TO ADD COURSE TO DATABASE
def add_course(course_id, name):
    name = name.upper()
    course_id = course_id.upper()
    sql = text("SELECT course_id FROM courses WHERE course_id = :course_id")
    sql2 = text("INSERT INTO Courses (course_id, name) VALUES (:course_id, :name)")
    course = db.session.execute(sql, {"course_id":course_id}).fetchone()
    
    if not course:
        db.session.execute(sql2, {"course_id":course_id, "name":name})
    
    db.session.commit()
    
# MODULE TO ADD REVIEW TO DATABASE
# TABLE REVIEW CONNECTED TO COURSES TABLE
# TABLES TEACHERS, MATERIAL, AND WORKLOAD CONNECTED TO REVIEWS
def add_review(course_id, material, workload, teacher_name, teacher_grade):
    course_id = course_id.upper()
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


# MODULES TO GATHER DATA FROM DATABASE

# MODULE RETURNING A LIST OF RECORDED COURSES
def get_courses():
    sql = text("SELECT course_id, name FROM Courses ORDER BY course_id")
    result = db.session.execute(sql)
    courses = result.fetchall()
    return courses

# MODULE RETURNING COURSE NAMES OF 5 LATEST REVIEWS
def latest_reviews():
    sql = text("SELECT C.name FROM reviews R, Courses C WHERE R.course = C.course_id ORDER BY created DESC LIMIT 5;")
    result = db.session.execute(sql)
    latest_reviews = result.fetchall()
    return latest_reviews

# MODULE RETURNING COURSE NAMES HAVING HIGHEST AVERAGE MATERIAL SCORE IN DESCENDING ORDER
def best_material():
    sql = text("""SELECT C.name
    FROM (SELECT W.grade AS w, R.course AS c FROM Workload W, Reviews R WHERE R.id = W.review_id) W, Courses C
    WHERE C.course_id = W.c
    GROUP BY C.course_id
    ORDER BY (SUM(W.w)/COUNT(W.w)) DESC;""")
    result = db.session.execute(sql)
    material = result.fetchall()
    return material