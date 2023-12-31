import secrets
import re
from flask import render_template, request, redirect, session, abort
from app import app
import database_control
import users
import stats



# HOMEPAGE
@app.route("/")
def index():
    reviewed_courses = stats.latest_reviews()
    material = stats.best_material()
    teacher = stats.best_teacher()
    workload = stats.best_workload()
    review_count = stats.count_reviews()
    return render_template("index.html", reviewed_courses=reviewed_courses, material=material,\
         teacher=teacher, workload=workload, review_count=review_count)



# ACCOUNT CREATION PAGE
@app.route("/newaccount", methods=["GET","POST"])
def newaccount():
    if request.method == "GET":
        return render_template("createaccount.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.create_user(username, password):
            return redirect("/login")
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
            if users.is_admin(username):
                session["admin"] = username + "admin"
                return redirect("/")
            return redirect("/")
        return render_template("loginpage.html", error_message=error_message)



# LOGOUT
# DELETE SESSIONS
@app.route("/logout")
def logout():
    if not session:
        abort(403)
    if users.is_admin(session["username"]):
        del session["admin"]
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

        try:
            course_name = re.search(r"\S\w*(:? \w+)*", course_name).group()
        except AttributeError:
            print("course name regex error")

        try:
            course_id = re.search(r"\S\w*-?\w*", course_id).group()
        except AttributeError:
            print("course id regex error")

        review_data = []
        teacher_name = request.form["teacher_name"]

        try:
            if re.search(r"\S[A-z]+ [A-z]+(, [A-z]+ [A-z]+)+", teacher_name):
                teacher_name = list(set(re.search(\
                    r"\S[A-z]+ [A-z]+(, *[A-z]+ [A-z]+)*", teacher_name)\
                        .group().split(", ")))
            else:
                teacher_name = re.search(r"\S\w* \w*", teacher_name).group()
        except AttributeError:
            print("teacher regex name error")
        review_data.append(teacher_name)
        review_data.append(request.form["teacher_grade"])
        review_data.append(request.form["material"])
        review_data.append(request.form["workload"])
        review_data.append(request.form["message"])
        database_control.add_course(course_id, course_name)
        if database_control.add_review(course_id, review_data):
            return render_template("result.html", course_id=course_id,\
            course_name=course_name, review_data=review_data)
        error = True
        return render_template("review.html", error=error)


# ROUTE TO SEARCH RESULTS
@app.route("/search", methods=["POST"])
def search():
    if session["csrf_token"]!=request.form["csrf_token"]:
        abort(403)
    unmodified_search_input = request.form["search_data"]

    try:
        search_input = re.search(r"\S\w*-?\w*", unmodified_search_input).group().upper()
        if stats.course_exists(search_input):
            course_data = stats.full_course_data(search_input)
            return render_template("search.html", courses=course_data)
    except AttributeError:
        pass

    try:
        search_input = re.search(r"\S\w* \w*", unmodified_search_input).group().upper()
        if stats.teacher_exists(search_input):
            teacher_data = stats.teacher_data(search_input)
            teacher_grade = stats.teacher_grades(search_input)
            return render_template("search.html", teacher=search_input,\
                teacher_data=teacher_data, teacher_grade=teacher_grade)
    except AttributeError:
        pass

    error = True
    courses = stats.latest_reviews()
    material = stats.best_material()
    teacher = stats.best_teacher()
    workload = stats.best_workload()
    review_count = stats.count_reviews()
    return render_template("index.html", courses=courses, material=material,\
        teacher=teacher, workload=workload,\
            review_count=review_count, error=error)



# FUNCTION TO RENDER THE TEACHER LIST PAGE
@app.route("/teachers")
def teachers():
    teachers = stats.get_teachers()
    teacher_count = stats.count_teachers()
    return render_template("teachers.html", teachers=teachers, teacher_count=teacher_count)



# FUNCTION TO RENDER THE COURSE LIST PAGE
@app.route("/courses")
def courses():
    courses = stats.get_courses()
    course_count = stats.count_courses()
    return render_template("courses.html", courses=courses, course_count=course_count)


# ROUTE TO PAGE WITH DATA ON THE RENAMED COURSE
# POSSIBILITY TO SHOW THE DELETE COURSE ROUTE AND QUESTION
@app.route("/renamed", methods=["POST"])
def rename():
    if session["csrf_token"]!=request.form["csrf_token"]:
        abort(403)
    delete_course = False
    try:
        new_name = request.form["new_name"]
        course_name = request.form["course_name"]
        course_id = request.form["course_id"]
        database_control.rename_course(course_id, new_name)
        return render_template("renamed.html", new_name=new_name,\
            course_id=course_id, course_name=course_name, delete_course=delete_course)
    except:
        course_name = request.form["course_name"]
        course_id = request.form["course_id"]
        delete_course = True

        return render_template("renamed.html", course_name=course_name,\
            course_id=course_id, delete_course=delete_course)
    return redirect("/")



#ROUTE TO THE DELETE.HTML FILE WITH INFO ON THE DELETED COURSE
@app.route("/delete", methods=["POST"])
def delete():
    if session["csrf_token"]!=request.form["csrf_token"]:
        abort(403)
    course_id = request.form["course_id"]
    database_control.delete_course(course_id)
    return render_template("delete.html", course_id=course_id)
