CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE Courses (course_id varchar PRIMARY KEY, name TEXT);
CREATE TABLE Reviews (id SERIAL PRIMARY KEY, course varchar REFERENCES Courses, created TIMESTAMP);
CREATE TABLE Teachers (id SERIAL PRIMARY KEY, name TEXT, grade FLOAT, review_id INTEGER REFERENCES Reviews);
CREATE TABLE Material (id SERIAL PRIMARY KEY, grade FLOAT, review_id INTEGER REFERENCES Reviews);
CREATE TABLE Workload (id SERIAL PRIMARY KEY, grade FLOAT, review_id INTEGER REFERENCES Reviews);
CREATE TABLE Review_messages (id SERIAL PRIMARY KEY, review_id INTEGER REFERENCES Reviews, message TEXT);
