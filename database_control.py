from sqlalchemy.sql import text
from db import db



# FUNCTIONS TO ADD DATA TO THE DATABASE

# FUNCTION TO ADD COURSE TO DATABASE
def add_course(course_id, name):
    name = name.upper()
    course_id = course_id.upper().strip()
    sql = text("SELECT course_id FROM courses WHERE course_id = :course_id")
    sql2 = text("INSERT INTO Courses (course_id, name) VALUES (:course_id, :name)")
    course = db.session.execute(sql, {"course_id":course_id}).fetchone()

    if not course:
        db.session.execute(sql2, {"course_id":course_id, "name":name})

    db.session.commit()

# FUNCTION TO ADD REVIEW TO DATABASE
# TABLE REVIEW CONNECTED TO COURSES TABLE
# TABLES TEACHERS, MATERIAL, AND WORKLOAD CONNECTED TO REVIEWS
def add_review(course_id, review_data):
    course_id = course_id.upper()
    sql = text("INSERT INTO Reviews (course, created) VALUES (:course_id, NOW())")
    db.session.execute(sql, {"course_id":course_id})
    db.session.commit()
    sql1 = text("SELECT MAX(id) FROM Reviews")
    reference = db.session.execute(sql1).fetchone()[0]
    try:
        sql2 = text("""INSERT INTO Teachers (name, grade, review_id)
            VALUES (:name, :grade, :review_id)""")
        sql3 = text("INSERT INTO Material (grade, review_id) VALUES (:grade, :review_id)")
        sql4 = text("""INSERT INTO Workload (grade, review_id)
            VALUES (:grade, :review_id)""")
        sql5 = text("""INSERT INTO Review_messages (review_id, message)
            VALUES (:review_id, :message)""")

        if type(review_data[0]) is list:
            for list_teacher_name in review_data[0]:
                list_teacher_name = list_teacher_name.upper()
                db.session.execute(sql2, {"name":list_teacher_name,\
                    "grade":review_data[1], "review_id":reference})

        else:
            teacher_name = review_data[0].upper()
            db.session.execute(sql2, {"name":teacher_name,\
                "grade":review_data[1], "review_id":reference})

        db.session.execute(sql3, {"grade":review_data[2], "review_id":reference})
        db.session.execute(sql4, {"grade":review_data[3], "review_id":reference})
        db.session.execute(sql5, {"review_id":reference, "message":review_data[4]})
        db.session.commit()
        return True
    except:
        exeption = text("DELETE FROM Reviews WHERE id=:review_id")
        db.session.execute(exeption, {"review_id":reference})
        db.session.commit()
        return False


# FUNCTION TO DELETE A COURSE AND
# ROWS FROM OTHER TABLES THAT REFERENCE TO IT
def delete_course(course_id):
    sql = text("DELETE FROM Courses WHERE course_id=:course_id")
    db.session.execute(sql, {"course_id":course_id})
    db.session.commit()


# RENAME COURSE ALLOW ADMIN TO RENAME COURSES
# IF A NAME IS INCORRECT OR INAPROPPRIATE
def rename_course(course_id, name):
    sql = text("UPDATE courses SET name=:name WHERE course_id=:course_id")
    db.session.execute(sql, {"name":name, "course_id":course_id})
    db.session.commit()
