from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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


##Need to make this so it redirects to the correct page admin or student
@app.route("/", methods=['POST','GET'])
def login():
    if request.method=='POST':
        
        user=request.form["txtUsername"]
        uPassword=request.form["txtPassword"]
    
        us = users.query.filter_by(netid=user).first()
        
        
        if us and us.password==uPassword:
             peop = people.query.filter_by(netid=user).first()
             return redirect(url_for("admin",name=peop.firstName))
           

        else:
           return render_template("login.html",error='Incorrect Login') 
            #return "There was an error"

    else:
        
        return render_template("login.html")
   


##Student view page
@app.route("/student")
def student():
    return render_template("student.html")


##Admin Page
@app.route("/admin/<name>")
def admin(name):
    return render_template("admin.html",name=name)

#Admin edit of student
@app.route("/adminStudent")
def adminStudent():
    return render_template("adminStudent.html")

##Admin Add Course
##Currently trying to get the form to commit
@app.route("/adminADD",methods=['POST','GET'])
def adminADD():
    ##FIX THIS SO ITS POST AND NOT GET
    if request.method=='GET':
        
        # courseTitle=request.form["courseTitle"]
        # CRN=request.form["CRN"]

    #     classCode=request.form["classCode"]
    #     maxE=request.form["maxEnrollment"]
    #     ##Set to zero on default
    #    ## enroll=request.form["enrollment"]
        
        
    #     courseSection=request.form["courseSection"]
    #     weekDay=request.form["weekDay"]
    #     startTime=request.form["startTime"]
    #     endTime=request.form["endTime"]
    #     profid=request.form["profid"]

    #     newCOURSE=(CRN,classCode,maxE,0,courseTitle,courseSection,weekDay,startTime,endTime,profid)
        newCOURSE=courses(CRN="0",classCode="0",maxEnrollment="0",enrollment="0",courseTitle="0",courseSection="0",weekDays="0",startTime="0",endTime="0",profid="0")
        db.session.add(newCOURSE)
        db.session.commit()
        return render_template("addCourses.html")
        

    else:
        return render_template("addCourses.html")










##Admin edit course
@app.route("/adminEDIT")
def adminEDIT():
    return render_template("adminEdit.html")

##Remove course
@app.route("/adminREMOVE")
def adminREMOVE():
    return render_template("removeCourses.html")

##Info On courses
@app.route("/adminINFO")
def adminINFO():
    return render_template("infoCourses.html")







if __name__=="__main__":
    app.run(debug=True)