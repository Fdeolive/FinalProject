import sqlite3 
import csv

#connect or create if doesn’t exist (same folder)
conn = sqlite3.connect('CS2990_Final_Project.db')

#create database cursor - enables traversal of records in db
cur = conn.cursor()

# Make sure to start with fresh tables
cur.execute("DROP TABLE IF EXISTS courses;")
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
# #create a table for posts csv
# cur.execute('''CREATE TABLE posts(user_id INTEGER, post TEXT, posted_date TEXT)''')

# # open file and add contents into table
# file = open('posts.csv')
# contents = csv.reader(file)
# headers = next(contents)

# insert_records = '''INSERT INTO posts('user_id','post','posted_date') VALUES(?,?,?)'''
# for row in contents:
#     if row!= []:
#         cur.execute(insert_records,row)
# # close the file
# file.close()

# #create a table for users csv
# cur.execute('''CREATE TABLE users(user_id INTEGER, email_id TEXT, username TEXT, password TEXT, account_created TEXT, first_name TEXT, last_name TEXT)''')

# # open file and add contents into table
# file = open('users.csv')
# contents = csv.reader(file)
# headers = next(contents)

# insert_records = '''INSERT INTO users('user_id','email_id','username','password','account_created','first_name','last_name') VALUES(?,?,?,?,?,?,?)'''
# for row in contents:
#     if row!= []:
#         cur.execute(insert_records,row)
# # close the file
# file.close()

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

