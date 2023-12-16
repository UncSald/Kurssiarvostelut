from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app

# DEFINE THE DATABASE FOR THE APP
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

db = SQLAlchemy(app)
