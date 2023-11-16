CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE Courses (course_id varchar PRIMARY KEY, name TEXT);
CREATE TABLE Reviews (id SERIAL PRIMARY KEY, course varchar REFERENCES Courses, created TIMESTAMP);
CREATE TABLE Teachers (id SERIAL PRIMARY KEY, name TEXT, grade INTEGER, review_id INTEGER REFERENCES Reviews);
CREATE TABLE Material (id SERIAL PRIMARY KEY, grade INTEGER, review_id INTEGER REFERENCES Reviews);
CREATE TABLE Workload (id SERIAL PRIMARY KEY, grade INTEGER, review_id INTEGER REFERENCES Reviews);
