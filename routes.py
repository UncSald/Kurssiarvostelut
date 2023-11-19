from app import app
import database_control
import users
import stats
from flask import render_template, request, redirect, session

# HOMEPAGE
@app.route("/")
def index():
    courses = stats.latest_reviews()
    material = stats.best_material()
    return render_template("index.html", courses=courses, material=material)


@app.route("/newaccount", methods = ["GET","POST"])

def newaccount():
    if request.method == "GET":
        return render_template("createaccount.html")
    if request.method == "POST":  
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
            return redirect("/")
        elif users.check_password(username, password) == 1:
            return render_template("error.html", message="Väärä salasana")
        elif users.check_password(username, password) == 0:
            return render_template("error.html", message="Väärä tunnus")
    

#LOGOUT
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

# REVIEW FORM
@app.route("/review")
def review():
    return render_template("review.html")

@app.route("/result", methods=["POST"])
def result():
    
    course_name = request.form["course_name"]
    course_id = request.form["course_id"]
    teacher_name = request.form["teacher_name"]
    teacher_grade = request.form["teacher_grade"]
    material = request.form["material"]
    workload = request.form["workload"]
    database_control.add_course(course_id, course_name)
    database_control.add_review(course_id, material, workload, teacher_name, teacher_grade)
    return render_template("result.html", course_id=course_id, course_name=course_name, teacher=teacher_grade, workload=workload, material=material)
