CREATE TABLE Courses (id SERIAL PRIMARY KEY, name TEXT, course_id TEXT);
CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE Course_grading (id SERIAL PRIMARY KEY, course_id integer REFERENCES Courses, material INTEGER, workload INTEGER, teacher INTEGER);