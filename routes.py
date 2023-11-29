from app import app
import database_control
import users
import stats
import secrets
from flask import render_template, request, redirect, session

# HOMEPAGE
@app.route("/")
def index():
    courses = stats.latest_reviews()
    material = stats.best_material()
    teacher = stats.best_teacher()
    workload = stats.best_workload()
    return render_template("index.html", courses=courses, material=material,\
         teacher=teacher, workload=workload)




@app.route("/newaccount", methods=["GET","POST"])
def newaccount():
    if request.method == "GET":
        return render_template("createaccount.html")
    if request.method == "POST":
        session.permanent = False
        username = request.form["username"]
        password = request.form["password"]
        users.create_user(username, password)
        return redirect("/login")

# LOGIN PAGE
# LOGIN CHECKS RETURNING 0, 1, OR 2 DEPENDING ON USERNAME NOT FOUND(0),
# WRONG PASSWORD(1) AND CORRECT USRNAME PASSWORD COMBO(2)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("loginpage.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.check_password(username, password) == 2:
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        elif users.check_password(username, password) == 1:
            return render_template("error.html", message="Väärä salasana")
        elif users.check_password(username, password) == 0:
            return render_template("error.html", message="Väärä tunnus")
    

# LOGOUT
# DELETE SESSIONS
@app.route("/logout")
def logout():
    del session["username"]
    del session["csrf_token"]
    return redirect("/")



# REVIEW FORM
@app.route("/review", methods=["GET", "POST"])
def result():
    if request.method == "GET":
        return render_template("review.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        course_name = request.form["course_name"]
        course_id = request.form["course_id"]
        teacher_name = request.form["teacher_name"]
        teacher_grade = request.form["teacher_grade"]
        material = request.form["material"]
        workload = request.form["workload"]
        message = request.form["message"]
        database_control.add_course(course_id, course_name)
        database_control.add_review(course_id, material, workload, teacher_name, teacher_grade, message)
        return render_template("result.html", course_id=course_id, course_name=course_name,\
             teacher=teacher_grade, workload=workload, material=material)



# ROUTE TO SEARCH RESULTS
@app.route("/search_course", methods=["POST"])
def search_course():
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
    courses = request.form["course_id"]
    if stats.course_exists(courses):
        courses = stats.full_course_data(courses)
        return render_template("search_course.html", courses=courses)
    return redirect("/")

    


@app.route("/search_teacher", methods=["POST"])
def search_teacher():
    if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
    teacher = request.form["teacher_name"].upper()
    if stats.teacher_exists(teacher):
        teacher_data = stats.teacher_data(teacher)
        teacher_grade = stats.teacher_grades(teacher)
        return render_template("search_teacher.html", teacher=teacher,\
             teacher_data=teacher_data, teacher_grade=teacher_grade)
    return redirect("/")