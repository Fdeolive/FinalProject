from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from datetime import datetime
##EDIT Admin
##ADMIn edit
##Fix Remove
##Get STD/Mean to work
##GRAPH

##Student add


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

@app.route("/student/<netid>")
def student(netid):
    ##Getting all the courses enrolled in
   if(request.method=='POST'):
       newCode=request.form["newCourse"]
       newCourse=enrollment(netid,CRN=newCode)
       db.session.add(newCourse)
       db.session.commit()
       results = db.session.query(courses.CRN,courses.courseTitle).join(enrollment, enrollment.CRN == courses.CRN, isouter=False).filter_by(netid=netid).all()
       return render_template("student.html",netid=netid,results=results)
   else:
    results = db.session.query(courses.CRN,courses.courseTitle).join(enrollment, enrollment.CRN == courses.CRN, isouter=False).filter_by(netid=netid).all()
    return render_template("student.html",netid=netid,results=results)



##Students information###
@app.route("/studentCourseINFO",methods=['POST','GET'])
def studentCourseINFO():

     if (request.method=="POST"):
        ###Figure this out the/Form content
        content=request.form.get("lstAnswer")
        
        
        if(content=="1"):
                    classes= db.session.query(people.netid,courses.profid,courses.courseTitle,courses.maxEnrollment,courses.enrollment,courses.weekDays,courses.startTime,courses.endTime,courses.CRN).join(courses, courses.profid == people.netid, isouter=False).filter(people.rating>3).all()
        elif(content=="2"):
                    classes= db.session.query(people.netid,courses.profid,courses.courseTitle,courses.maxEnrollment,courses.enrollment,courses.weekDays,courses.startTime,courses.endTime,courses.CRN).join(courses, courses.profid == people.netid, isouter=False).filter(people.rating>3.5).all()
        elif(content=="3"):
                    classes= db.session.query(people.netid,courses.profid,courses.courseTitle,courses.maxEnrollment,courses.enrollment,courses.weekDays,courses.startTime,courses.endTime,courses.CRN).join(courses, courses.profid == people.netid, isouter=False).filter(people.rating>4).all()
        elif(content=="4"):
                    classes= db.session.query(people.netid,courses.profid,courses.courseTitle,courses.maxEnrollment,courses.enrollment,courses.weekDays,courses.startTime,courses.endTime,courses.CRN).join(courses, courses.profid == people.netid, isouter=False).filter(people.rating>4.5).all()
        elif(content=="5"):
            classes = courses.query.filter(courses.weekDays == 'MWF')
        elif(content=="6"):
            classes = courses.query.filter(courses.weekDays == 'TTh')    
        elif(content=="7"):
            classes = courses.query.filter(courses.maxEnrollment > courses.enrollment)   
            
        return render_template("studentCourseINFO.html",classes=classes,content=content)
   
     else: 
        
   
        classes = courses.query.all()
        content=0
        return render_template("studentCourseINFO.html",classes=classes,content=content)

@app.route("/studentCourseREMOVE/<CRN>")
def studentCourseREMOVE (CRN):
    enroll = enrollment.query.get_or_404(CRN)
    try:
        db.session.delete(enroll)
        db.session.commit()
        return render_template('studentCourseEDIT.html')
    except:
        return 'There was a problem deleting that course'
    


################################ADMIN PAGE#####################################################

@app.route("/admin/<name>")
def admin(name):
    return render_template("admin.html",name=name)


@app.route("/adminStudent")
def adminStudent():
    student = people.query.filter_by(type="S").all()
    return render_template('adminStudent.html', student=student)

#Admin edit of student
@app.route("/adminStudentINFO/<netid>")
def adminStudentInfo(netid):
    student = people.query.get_or_404(netid)
    # if request.method=='POST':
    #     answer=student.GPA
    course=enrollment.query.filter(enrollment.netid==netid)
    return render_template("adminStudentINFO.html",student=student,course=course)


@app.route("/adminStudentEdit/<netid>")
def adminStudentEdit(netid):
    student = people.query.get_or_404(netid)

    #Gets the info from the selected student
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
        return render_template('adminStudentEdit.html', student=student)

##Admin Add Course
#Admin Add Course
@app.route("/adminADD",methods=['POST','GET'])
def adminADD():
    
    if request.method=='POST':
        
        # ##Get from the form
        # courseTitle=request.form["courseTitle"]
        # CRN=request.form["CRN"]
        # classCode=request.form["classCode"]
        # maxE=request.form["maxEnrollment"]
        # courseSection=request.form["courseSection"]
        # weekDay=request.form["weekDay"]
        # startTime=request.form["startTime"]
        # endTime=request.form["endTime"]
        # profid=request.form["profid"]
        ##Adds to the database 
        newCOURSE=courses(CRN="0",classCode="0",maxEnrollment="0",enrollment="0",courseTitle="0",courseSection="0",weekDays="0",startTime="0",endTime="0",profid="0")
        #newCOURSE=courses(CRN=CRN,classCode=classCode,maxEnrollment=maxE,enrollment="0",courseTitle=courseTitle,courseSection=courseSection,weekDays=weekDay,startTime=startTime,endTime=endTime,profid=profid)
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
            return redirect(url_for("adminCourses"))
        
        except:
            return 'There was an issue updating your course'

    else:
        return render_template('adminEDIT.html', course=course)


##Remove course
@app.route("/adminREMOVE/<CRN>")
def adminREMOVE(CRN):
    classes = courses.query.get_or_404(CRN)
    try:
        db.session.delete(classes)
        db.session.commit()
        return render_template('adminCourse.html')
    except:
        return 'There was a problem deleting that course'

#--------------------------------------------------------------------------------------#
@app.route("/adminCourseINFO/<CRN>", methods=['GET','POST'])
def adminCourseINFO(CRN):
    ###Figure out how to display on the screen
    if (request.method=="POST"):
        content=request.form.get("math")
        
        print(content)

        if content=='1':
            answers= db.session.query(db.func.sum(enrollment.netid)).filter(enrollment.CRN==CRN).first()

        elif content=='2':    
            answer=db.session.query(db.func.avg(people.GPA)).join(enrollment, enrollment.netid == people.netid).filter(enrollment.CRN==CRN).first()
        
        elif content=='3':    
            answer=db.session.query(db.func.max(people.GPA)).join(enrollment, enrollment.netid == people.netid).filter(enrollment.CRN==CRN).first()
        elif content=='4':    
            answer=db.session.query(db.func.min(people.GPA)).join(enrollment, enrollment.netid == people.netid).filter(enrollment.CRN==CRN).first()
        
        elif content=='5':    
            answer=db.session.query(db.func.stddev(people.GPA)).join(enrollment, enrollment.netid == people.netid).filter(enrollment.CRN==CRN).first()
        
        else:
            answer=0
        return render_template("adminCourseINFO.html",answer=answer, CRN=CRN)
   
    else:  
       answer=0
       return render_template("adminCourseINFO.html",answer=answer,CRN=CRN)


if __name__=="__main__":
    app.run(debug=True)