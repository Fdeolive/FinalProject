import matplotlib.pyplot as plt
import numpy as np
import sqlite3

conn = sqlite3.connect('CS2990_Final_Project.db')
cur = conn.cursor()
cur.execute("SELECT count(*), courseTitle FROM enrollment JOIN courses ON enrollment.CRN = courses.CRN GROUP BY courseTitle ORDER BY count(*)")
enrollment = cur.fetchall()
enroll_data = []
course_titles = []
num_classes = 1
x_axis = []
for row in enrollment:
    enroll_data.append(row[0])
for row in enrollment:
    course_titles.append(row[1])
    x_axis.append(num_classes)
    num_classes += 1
fig, ax = plt.subplots()
plt.xticks(x_axis,course_titles)

ax.set_xticklabels(course_titles, rotation=45)
ax.scatter(x_axis,enroll_data)
ax.set_title("Enrollment")
#plt.show()
fig.savefig("EnrollmentGraph.png")

cur.execute("SELECT AVG(people.gpa), courseTitle FROM courses JOIN enrollment ON courses.CRN = enrollment.CRN JOIN people on enrollment.netid = people.netid GROUP BY courseTitle ORDER BY people.gpa ")
gpas = cur.fetchall()
gpa_data = []
course_titles = []
num_classes = 1
x_axis = []
for row in gpas:
    gpa_data.append(row[0])
    x_axis.append(num_classes)
    num_classes += 1
for row in gpas:
    course_titles.append(row[1])
fig2, ax = plt.subplots()
plt.xticks(x_axis,course_titles)

ax.set_xticklabels(course_titles, rotation=45)
ax.scatter(x_axis,gpa_data)
ax.set_title("GPA By Class")
#plt.show()
fig.savefig("GPAGraph.png")