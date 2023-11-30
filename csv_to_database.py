import sqlite3 
import csv

#connect or create if doesn’t exist (same folder)
conn = sqlite3.connect('CS2990_Final_Project.db')

#create database cursor - enables traversal of records in db
cur = conn.cursor()

# Make sure to start with fresh tables
cur.execute("DROP TABLE IF EXISTS courses;")
cur.execute("DROP TABLE IF EXISTS users;")
cur.execute("DROP TABLE IF EXISTS people;")
# TODO: REPLACE TABLES WITH RELEVANT NAMES
# cur.execute("DROP TABLE IF EXISTS posts;")
# cur.execute("DROP TABLE IF EXISTS users;")


# create a table for courses csv
cur.execute('''CREATE TABLE courses(CRN INTEGER, classCode TEXT, maxEnrollment INTEGER, enrollment INTEGER, courseTitle TEXT, courseSection TEXT, weekDays TEXT, startTime TIME, endTime TIME)''')

# open file and add contents into table
file = open('courses.csv')
contents = csv.reader(file)
headers = next(contents)

insert_records = '''INSERT INTO courses('CRN','classCode','maxEnrollment','enrollment','courseTitle','courseSection','weekDays','startTime','endTime') VALUES(?,?,?,?,?,?,?,?,?)'''
for row in contents:
    if row!= []:
        cur.execute(insert_records,row)
# close the file
file.close()

# TODO: UPDATE FOR RELEVANT TABLES 
# create a table for users csv
cur.execute('''CREATE TABLE users(netid TEXT, password TEXT)''')

# for users data, we used randomly generated names and passwords from these sources:
# https://www.behindthename.com/random/random.php?gender=both&number=2&sets=1&surname=&norare=yes&usage_eng=1
# https://www.dinopass.com/
# open file and add contents into table
file = open('users.csv')
contents = csv.reader(file)
headers = next(contents)

insert_records = '''INSERT INTO users('netid','password') VALUES(?,?)'''
for row in contents:
    if row != []:
        cur.execute(insert_records, row)
# close the file
file.close()

# create a table for people csv
cur.execute('''CREATE TABLE people(firstName TEXT, lastName TEXT, netid TEXT, hold TEXT, type TEXT, rating FLOAT, gpa FLOAT)''')

# for people data, we used randomly generated names from this source:
# https://www.behindthename.com/random/random.php?gender=both&number=2&sets=1&surname=&norare=yes&usage_eng=1
# open file and add contents into table
file = open('people.csv')
contents = csv.reader(file)
headers = next(contents)

insert_records = '''INSERT INTO people('firstName','lastName','netid','hold','type','rating','gpa') VALUES(?,?,?,?,?,?,?)'''
for row in contents:
    if row != []:
        cur.execute(insert_records, row)
# close the file
file.close()

conn.commit()

#let's check what's in there
data = cur.execute("SELECT * FROM courses")
print(data.fetchall())
# TODO: UPDATE FOR RELEVANT TABLES 
# data = cur.execute("SELECT * FROM posts")
# print(data.fetchall())
# data = cur.execute("SELECT * FROM users")
# print(data.fetchall())



conn.commit()
conn.close()

