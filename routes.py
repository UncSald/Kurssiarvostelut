from app import app
import database_control
from flask import render_template, request


@app.route("/")
def index():
    courses = database_control.get_courses()
    return render_template("index.html", courses=courses)

@app.route("/review")
def review():
    return render_template("review.html")

@app.route("/result", methods=["POST"])
def result():
    course_name = request.form["course_name"]
    course_id = request.form["course_id"]
    opettaja = request.form["opettaja"]
    database_control.add_course(course_name, course_id)
    return render_template("result.html", course_name=course_name, course_id=course_id, opettaja=opettaja)