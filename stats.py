from db import db
from sqlalchemy.sql import text

# FUNCTION RETURNING A LIST OF RECORDED COURSES
def get_courses():
    sql = text("SELECT course_id, name FROM Courses ORDER BY course_id")
    result = db.session.execute(sql)
    courses = result.fetchall()
    return courses

# FUNCTION RETURNING COURSE NAMES OF 5 LATEST REVIEWS
def latest_reviews():
    sql = text("SELECT C.name FROM reviews R, Courses C WHERE R.course = C.course_id ORDER BY created DESC LIMIT 5;")
    result = db.session.execute(sql)
    latest_reviews = result.fetchall()
    return latest_reviews

# FUNCTION RETURNING COURSE NAMES HAVING HIGHEST AVERAGE MATERIAL SCORE IN DESCENDING ORDER
def best_material():
    sql = text("""SELECT C.name
    FROM (SELECT W.grade AS w, R.course AS c FROM Material W, Reviews R WHERE R.id = W.review_id) W, Courses C
    WHERE C.course_id = W.c
    GROUP BY C.course_id
    ORDER BY (SUM(W.w)/COUNT(W.w)) DESC LIMIT 5;""")
    result = db.session.execute(sql)
    material = result.fetchall()
    return material