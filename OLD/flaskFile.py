from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

##Connectiong to the existing database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CS2990_Final_Project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##The model for the tables
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(200), nullable=False)
    password= db.Column(db.String(200), nullable=False)

class people(db.Model):
    firstName=db.Column(db.String(200), nullable=False)
    lastName=db.Column(db.String(200), nullable=False)
    netid=db.Column(db.String(200), primary_key=True)
    hold=db.Column(db.String(200), nullable=False)
    type=db.Column(db.String(200), nullable=False)
    rating=db.Column(db.String(200), nullable=False)
    gpa=db.Column(db.String(200), nullable=False)

#     ##stuff

# class Enrollement(db.Model):
#     ##stuff

# class Courses(db.Model):
#     ##stuff

##Default login page
@app.route('/', methods=['POST', 'GET'])

def Login():
    if request.method == 'POST':
        ##Getting the info
        ##MAYBE
        userName = request.form['userName']
        password = request.form['password']

        user = users.query.filter_by(username=userName).first()

    # if  user.check_password(password):
    #     # Authentication successful
    #     # You can store the user's information in a session or perform other actions
    #    personType=people.query.filter_by(netid=userName).with_entities(people.type).first()
    #    if personType:
    #        if personType.type=="student":
    #         #return redirect(url_for('MYUVM'))
    #         return render_template('login.php', error='Login')
    #        elif personType.type=="teacher" :
    #         #return redirect(url_for('ADMIN'))    
    #         return render_template('login.php', error='Login')
           
    #   ## return redirect(url_for('success'))
        
       
    # else:
    #     # Authentication failed
    #    return render_template('login.php', error='Invalid username or password')


# # ##Student view
# # ##Shows the students classes by default 
# # ##Has buttons and stuff
# # @app.route('/', methods=['POST', 'GET'])


# # ##Admin View





        

# @app.route('/delete/<int:id>')
# def delete(id):
#     Participant_to_delete = Participant.query.get_or_404(id)

#     try:
#         db.session.delete(Participant_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'There was a problem deleting that participant'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     person = Participant.query.get_or_404(id)

#     if request.method == 'POST':
#         Participant.firstName = request.form['firstName']
#         Participant.lastName = request.form['lastName']
#         Participant.title = request.form['title']
#         Participant.type = request.form['type']
#         Participant.state = request.form['state']
#         Participant.city = request.form['city']
#         Participant.zip = request.form['zip']
#         Participant.phoneNumber = request.form['phoneNumber']
#         Participant.country = request.form['country']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'There was an issue updating the participant'

#     else:
#         return render_template('update.html', Participant=Participant)


if __name__ == "__main__":
    app.run(debug=True)

