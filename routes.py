import secrets
from flask import render_template, request, redirect, session, abort
from app import app
import database_control
import users
import stats



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
        if not users.create_user(username, password):
            return redirect("/login")
        else:
            error = True
            return render_template("createaccount.html", error=error)
# LOGIN PAGE
# LOGIN CHECKS RETURNING TRUE OR FALSE
@app.route("/login", methods=["GET", "POST"])
def login():
    error_message = "Käyttäjätunnus tai salasana on väärä"
    if request.method == "GET":
        return render_template("loginpage.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.check_password(username, password):
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        return render_template("loginpage.html", error_message=error_message)



# LOGOUT
# DELETE SESSIONS
@app.route("/logout")
def logout():
    if not session:
        abort(403)
    del session["username"]
    del session["csrf_token"]
    return redirect("/")



# REVIEW FORM
@app.route("/review", methods=["GET", "POST"])
def result():
    if not session:
        abort(403)
    if request.method == "GET":
        return render_template("review.html")
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        course_name = request.form["course_name"]
        course_id = request.form["course_id"]
        review_data = []
        review_data.append(request.form["teacher_name"])
        review_data.append(request.form["teacher_grade"])
        review_data.append(request.form["material"])
        review_data.append(request.form["workload"])
        review_data.append(request.form["message"])
        database_control.add_course(course_id, course_name)
        database_control.add_review(course_id, review_data)
        return render_template("result.html", course_id=course_id, course_name=course_name,\
             review_data=review_data)



# ROUTE TO SEARCH RESULTS
@app.route("/search", methods=["POST"])
def search():
    if session["csrf_token"]!=request.form["csrf_token"]:
        abort(403)
    search_input = request.form["search_data"]
    search_input = search_input.upper()
    if stats.course_exists(search_input):
        course_data = stats.full_course_data(search_input)
        return render_template("search.html", courses=course_data)
    if stats.teacher_exists(search_input):
        teacher_data = stats.teacher_data(search_input)
        teacher_grade = stats.teacher_grades(search_input)
        return render_template("search.html", teacher=search_input,\
             teacher_data=teacher_data, teacher_grade=teacher_grade)
    error = True
    return render_template("index.html", error=error)



# FUNCTION TO RENDER THE TEACHER LIST PAGE
@app.route("/teachers")
def teachers():
    teachers = stats.get_teachers()
    return render_template("teachers.html", teachers=teachers)



# FUNCTION TO RENDER THE COURSE LIST PAGE
@app.route("/courses")
def courses():
    courses = stats.get_courses()
    return render_template("courses.html", courses=courses)