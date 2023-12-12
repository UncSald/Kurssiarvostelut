from sqlalchemy.sql import text
from db import db


# FUNCTION RETURNING A LIST OF RECORDED COURSES
def get_courses():
    sql = text("SELECT course_id, name FROM Courses ORDER BY course_id")
    result = db.session.execute(sql)
    courses = result.fetchall()
    return courses



# FUNCTION RETURNING ALL TEACHERS REGISTERED IN THE DATABASE
def get_teachers():
    sql = text("SELECT name FROM Teachers GROUP BY name ORDER BY name")
    result = db.session.execute(sql)
    teachers = result.fetchall()
    return teachers




# FUNCTION RETURNING COURSE NAMES OF 5 LATEST REVIEWS
def latest_reviews():
    sql = text("""SELECT C.name, C.course_id
                    FROM Reviews R, Courses C
                    WHERE R.course = C.course_id
                    ORDER BY created
                    DESC LIMIT 5;""")
    result = db.session.execute(sql).fetchall()
    return result



# GET FULL COURSE DATA
def full_course_data(course_id):
    course_id = course_id.upper().strip()
    sql = text("""SELECT C.name, C.course_id, T.name, T.grade, M.grade, W.grade, RM.message
                    FROM Courses C 
                    JOIN Reviews R ON C.course_id=R.course AND C.course_id = :course_id
                    LEFT JOIN Teachers T ON T.review_id = R.id
                    LEFT JOIN Material M ON R.id = M.review_id
                    LEFT JOIN Workload W ON R.id = W.review_id
                    LEFT JOIN Review_messages RM ON RM.review_id = R.id;""")

    result = db.session.execute(sql, {"course_id":course_id}).fetchall()
    return result



# FUNCTION RETURNING COURSE NAMES HAVING HIGHEST AVERAGE MATERIAL SCORE IN DESCENDING ORDER
def best_material():
    sql = text("""SELECT C.name, C.course_id, (SUM(W.w)/COUNT(W.w))
                    FROM (SELECT W.grade AS w, R.course AS c
                            FROM Material W, Reviews R
                            WHERE R.id = W.review_id) W, Courses C
                    WHERE C.course_id = W.c
                    GROUP BY C.course_id
                    ORDER BY (SUM(W.w)/COUNT(W.w)) DESC LIMIT 5;""")
    result = db.session.execute(sql)
    material = result.fetchall()
    return material



# RETURN THE NAME OF THE BEST TEACHER
def best_teacher():
    sql = text("""SELECT W.n, (SUM(W.w)/COUNT(W.w))
                    FROM (SELECT W.grade AS w, R.course AS c, W.name AS n 
                            FROM Teachers W, Reviews R 
                            WHERE R.id = W.review_id) W
                    GROUP BY W.n
                    ORDER BY (SUM(W.w)/COUNT(W.w)) DESC LIMIT 5;""")
    result = db.session.execute(sql)
    teachers = result.fetchall()
    return teachers




def best_workload():
    sql = text("""SELECT C.name, C.course_id, (SUM(W.w)/COUNT(W.w))
                    FROM (SELECT W.grade AS w, R.course AS c
                            FROM Workload W, Reviews R
                            WHERE R.id = W.review_id) W, Courses C
                    WHERE C.course_id = W.c
                    GROUP BY C.course_id
                    ORDER BY (SUM(W.w)/COUNT(W.w)) DESC LIMIT 5;""")
    result = db.session.execute(sql)
    workload = result.fetchall()
    return workload




def best_overall():
    sql = text("")
    result = db.session.execute(sql)
    best = result.fetchall()
    return best




def course_exists(course_id):
    course_id=course_id.upper()
    sql = text("SELECT course_id FROM Courses WHERE course_id = :course_id")
    result = db.session.execute(sql, {"course_id":course_id}).fetchone()
    return bool(result)




def teacher_exists(teacher_name):
    teacher_name = teacher_name.upper()
    sql = text("SELECT name FROM Teachers WHERE name = :name")
    result = db.session.execute(sql, {"name":teacher_name}).fetchone()
    return bool(result)




def teacher_data(teacher_name):
    sql = text("""SELECT T.name ,T.grade, C.course_id   FROM Teachers T
                    JOIN Reviews R ON R.id = T.review_id
                        AND T.name LIKE :teacher_name
                    LEFT JOIN Courses C ON R.course = C.course_id;""")
    result = db.session.execute(sql, {"teacher_name":teacher_name}).fetchall()
    return result




def teacher_grades(teacher_name):
    sql = text("""SELECT SUM(grade)/COUNT(grade)
                    FROM Teachers
                    WHERE name = :teacher_name""")
    result = db.session.execute(sql, {"teacher_name":teacher_name}).fetchone()
    return result
