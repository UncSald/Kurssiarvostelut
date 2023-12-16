DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS Teachers CASCADE;
DROP TABLE IF EXISTS Material CASCADE;
DROP TABLE IF EXISTS Workload CASCADE;
DROP TABLE IF EXISTS Review_messages CASCADE;

CREATE TABLE Users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, rights BOOLEAN);
CREATE TABLE Courses (course_id varchar PRIMARY KEY, name TEXT);
CREATE TABLE Reviews (id SERIAL PRIMARY KEY, course varchar REFERENCES Courses ON DELETE CASCADE, created TIMESTAMP);
CREATE TABLE Teachers (id SERIAL PRIMARY KEY, name TEXT, grade FLOAT, review_id INTEGER REFERENCES Reviews ON DELETE CASCADE);
CREATE TABLE Material (id SERIAL PRIMARY KEY, grade FLOAT, review_id INTEGER REFERENCES Reviews ON DELETE CASCADE);
CREATE TABLE Workload (id SERIAL PRIMARY KEY, grade FLOAT, review_id INTEGER REFERENCES Reviews ON DELETE CASCADE);
CREATE TABLE Review_messages (id SERIAL PRIMARY KEY, review_id INTEGER REFERENCES Reviews ON DELETE CASCADE, message TEXT);

--Add admin user. USERNAME: admin PASSWORD: kurssikarhu
INSERT INTO Users (username, password, rights) VALUES ('admin',
'scrypt:32768:8:1$LO4eIHwkM14dvFBD$c9c96ba44e4c6ab0f71bd7b1b7c6bc4146c2af0ea6c6d74fafe86f7fdf101d601aefeedaac0ccf483183b51e2c5a0dde68a16f71617b82d7205a5043491dbff1',
'True')