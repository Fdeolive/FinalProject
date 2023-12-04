from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
##STILL TO DO:
###GEt the home nav to work 
######Get the student home page to join the course table 
###Add the info page on student and admin
###This is where all the stuff are going to be
######Need to include graphs
##Do CSS
####Include logout button


##Creating the flask 
app=Flask(__name__)
##Adding the database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///CS2990_Final_Project.db'

db=SQLAlchemy(app)

##Model 
class users(db.Model):
    netid=db.Column(db.String(200),primary_key=True)
    password=db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<netid %r>' % self.netid

class people(db.Model):
     firstName=db.Column(db.String(200),nullable=False)
     lastName=db.Column(db.String(200),nullable=False)
     hold=db.Column(db.String(200),nullable=False)
     type=db.Column(db.String(200),nullable=False)
     rating=db.Column(db.String(200),nullable=True)
     GPA=db.Column(db.String(200),nullable=True)
     netid=db.Column(db.String(200),primary_key=True)

     def __repr__(self):
        return '<netid %r>' % self.netid

class courses(db.Model):
    CRN=db.Column(db.String(200),primary_key=True,unique=True)
    classCode=db.Column(db.String(200),nullable=False)
    maxEnrollment=db.Column(db.Integer,nullable=False)
    enrollment=db.Column(db.Integer,nullable=False)
    courseTitle=db.Column(db.String(200),nullable=True)
    courseSection=db.Column(db.String(200),nullable=True)
    weekDays=db.Column(db.String(200),nullable=True)
    startTime=db.Column(db.String(200),nullable=True)
    endTime=db.Column(db.String(200),nullable=True)
    profid=db.Column(db.String(200),nullable=True)

    def __repr__(self):
        return '<CRN %r>' % self.CRN

class enrollment(db.Model):
   #  ID=db.Column(db.Integer,primary_key=True)
     CRN=db.Column(db.String(200),primary_key=True)
     netid=db.Column(db.String(200),primary_key=True)


     def __repr__(self):
        return '<CRN %r>' % self.CRN
    

@app.route("/", methods=['POST','GET'])
def login():
    if request.method=='POST':
        
        user=request.form["txtUsername"]
        uPassword=request.form["txtPassword"]
    
        us = users.query.filter_by(netid=user).first()
        
        
        if us and us.password==uPassword:
             peop = people.query.filter_by(netid=user).first()
             peopType=people.query.filter_by(netid=user).with_entities(people.type).scalar()
             if peopType=="A":
                return redirect(url_for("admin",name=peop.firstName))
             else:
                 return redirect(url_for("student",netid=user))
           

        else:
           return render_template("login.html",error='Incorrect Login') 
            #return "There was an error"

    else:
        
        return render_template("login.html")
   

########################################### STUDENT PAGE################################################

##potentially do credits
@app.route("/student/<netid>")
def student(netid):
    ##Getting all the courses enrolled in
   # coursesEnrolled = enrollment.query.filter_by(netid=netid).all()

    ##Select * from courses join enrollment on crn where netid=netid
    ##Getting the CRN for the courses enrolled in


    #result = courses.query.join(enrollment).filter(courses.CRN == enrollment.CRN).all()
   # result = db.session.query(courses,enrollment).left_join(enrollment).filter_by(courses.CRN == enrollment.CRN).filter_by(netid=netid).all()
    #result = db.session.query(courses,enrollment).select_from(courses).join(enrollment).filter_by(netid=netid).all()
   # result=db.select_from(db.join(courses, enrollment, isouter=True))
   results = db.session.query(courses,enrollment).join(courses, courses.CRN == enroll.CRN, isouter=False).filter_by(netid=netid).all()
   # Iterate results and do stuff
    #courseInfo=courses.query(CRN)
   return render_template("student.html",netid=netid,results=results)

@app.route("/studentCourseEDIT")
def studentCourseEDIT():
    return render_template("studentCourseEDIT.html")

@app.route("/studentCourseINFO")
def studentCourseINFO():
    return render_template("studentCourseINFO.html")


################################ADMIN PAGE#####################################################
@app.route("/admin/<name>")
def admin(name):
    return render_template("admin.html",name=name)


@app.route("/adminStudent")
def adminStudent():
    student = people.query.filter_by(type="S").all()
    return render_template('adminStudent.html', student=student)

#Admin edit of student
@app.route("/adminStudentInfo")
def adminStudentInfo():
    return render_template("adminStudent.html")


@app.route("/adminStudentEdit/<netid>")
def adminStudentEdit(netid):
    student = people.query.get_or_404(netid)

    #Gets the info from the selected course
    if request.method == 'POST':
        student.firstName=request.form["firstName"]
        student.lastName=request.form["lastName"]
        student.hold=request.form["hold"]
        student.GPA=request.form["gpa"]

        try:
            db.session.commit()
            return redirect(url_for("adminStudent"))
        
        except:
            return 'There was an issue updating the students information'

    else:
        return render_template('adminStudentEdit.html', netid=netid)

##Admin Add Course
@app.route("/adminADD",methods=['POST','GET'])
def adminADD():
    
    if request.method=='POST':
        
        ##Get from the form
        courseTitle=request.form["courseTitle"]
        CRN=request.form["CRN"]
        classCode=request.form["classCode"]
        maxE=request.form["maxEnrollment"]
        courseSection=request.form["courseSection"]
        weekDay=request.form["weekDay"]
        startTime=request.form["startTime"]
        endTime=request.form["endTime"]
        profid=request.form["profid"]


        ##Adds to the database 
        newCOURSE=courses(CRN=CRN,classCode=classCode,maxEnrollment=maxE,enrollment="0",courseTitle=courseTitle,courseSection=courseSection,weekDays=weekDay,startTime=startTime,endTime=endTime,profid=profid)
        db.session.add(newCOURSE)
        db.session.commit()
        return render_template("addCourses.html")
    else:
        return render_template("addCourses.html")


##Displays all the course
@app.route("/adminCourses")
def adminCourse():
    course = courses.query.all()
    return render_template('adminCourse.html', course=course)


##Admin edit course
@app.route("/adminEDIT/<CRN>")
def adminEDIT(CRN):
    course = courses.query.get_or_404(CRN)

    #Gets the info from the selected course
    if request.method == 'POST':
        course.courseTitle=request.form["courseTitle"]
        course.CRN=course.CRN
        course.enrollment=course.enrollment
        course.classCode=request.form["classCode"]
        course.maxE=request.form["maxEnrollment"]
        course.courseSection=request.form["courseSection"]
        course.weekDay=request.form["weekDay"]
        course.startTime=request.form["startTime"]
        course.endTime=request.form["endTime"]
        course.profid=request.form["profid"]

        try:
            db.session.commit()
            return redirect(url_for("adminCourse"))
        
        except:
            return 'There was an issue updating your course'

    else:
        return render_template('adminEDIT.html', course=course)


##Remove course
##Need to add like if more less than 1/3 then can't remove
@app.route("/adminREMOVE/<CRN>")
def adminREMOVE(CRN):
    classes = courses.query.get_or_404(CRN)
    try:
        db.session.delete(classes)
        db.session.commit()
        return render_template('adminCourse.html')
    except:
        return 'There was a problem deleting that course'

##Info On courses
@app.route("/adminINFO")
def adminINFO():
    return render_template("infoCourses.html")



if __name__=="__main__":
    app.run(debug=True)