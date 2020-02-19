# This is the main python file for the web application
# The other files refer to this page as the routing page

###################################################################################
# For the application to be run, the command line is required
# in my instance it was : cd Documents/Flask App
# This creates the directory
#                                                                                 
# py -m venv env
# env\Scripts\activate
# This creates the virtual environments required to install flask and run it
#                                                                                  
# finally
# set FLASK_APP=app.py
# This means that when app.py is run in the command line, the location where the app
# Is Running is created and then ready to be pasted into the url
######################################################################################


# SQLAlchemy handles the database
from datetime import datetime

# I imported render_template, which combines the app route to a html page created in a different file
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

# datetime allows the date the employee picks to be saved in the

app = Flask(__name__)

# app.config for the database below is set to false so there isn't a message sent everytime thre is a change to the
# database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config below is where the database is stored using mysql the first part is the server name.
# After the : is the server password and following that is the web servers name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

# setting the database to be accessed later under db rather than the whole SQLAlchemy library
db = SQLAlchemy(app)
db.app = app


# I create a class that will create a database model of all the bookings
class Booking(db.Model):
    # id is the primary key for the table .Column gives it the header in the table
    id = db.Column(db.Integer, primary_key=True)
    # first name (fname) has a max string length of 50
    fname = db.Column(db.String(50))
    # last name (lname) has a max string length of 50
    lname = db.Column(db.String(50))
    # email has a max string length of 50
    email = db.Column(db.String(50))
    # room will be saved as an integer
    room = db.Column(db.Integer)
    # date has its own data type of DateTime
    date = db.Column(db.DateTime)


class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signupresult', methods=['POST'])
def signupresult():
    db.create_all()
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']
    record = Members(fname=fname, lname=lname, email=email, password=password)
    db.session.add(record)
    db.session.commit()
    result = Members.query.all()
    return render_template('signupresult.html', fname=fname, lname=lname, email=email, password=password,
                           result=result)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/loginresult', methods=['POST'])
def loginresult():
    # TODO login handling
    return render_template('loginresult.html')


@app.route('/home')
def home():
    return render_template('home.html')


# This is the first app route
# Nothing follows the '/' which means that this is the landing page once the code is run
@app.route('/')
# a function index is created
# index is a common name given to the landing page of a web application
def index():
    # using the render_template imported earlier
    # the html page associated with what should be shown is called 'home.html'
    return render_template('sign.html')


# Another app route  is defined with the function about
# This route is called if the url of the web application is '/about'
@app.route('/about')
def about():
    # The page about.html is rendered and called
    return render_template('about.html')


# Another app route  is defined with the function bookings
# This route is called if the url of the web application is '/bookings'
@app.route('/bookings')
def bookings():
    # The page bookings.html is rendered and called
    return render_template('bookings.html')


# Here is a route for the feedback of the form
# The route is called if the url web application is '/feedback'
# Method of POST is used in html for when the data returned by a page is saved and enclosed within that page
# Setting it's method to POST, means that it can receive what the user entered
@app.route('/feedback', methods=['POST'])
# A feedback function is called
def feedback():
    # Below, all the fields filled out in the booking form
    # Using the request module that was imported at the top
    # Each individual is requested an dthe value associated with that specific form is stored in it
    db.create_all()
    # need to format HTML date into python's datetime
    formDateData = request.form['date']

    print("Date -> " + formDateData)

    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    room = request.form['room']
    date = datetime.strptime(formDateData, '%Y-%m-%d')  # second parameter is local representation of the string
    # The make is in respect to the records class created earlier
    # The variables and values associated are all passed in to add to a databse table
    record = Booking(fname=fname, lname=lname, email=email, room=room, date=date)
    # db.session starts a new entry and then the commit function adds them
    db.session.add(record)
    db.session.commit()
    # a variable result is created which requests the entire contents of the table
    # hence the query.all()
    result = Booking.query.all()
    # feedback template is called and variables needed in the feedback template are also passed in
    # result is sent in so the entire tables contents can be referenced
    return render_template('feedback.html', fname=fname, lname=lname, email=email, room=room, date=date, result=result)


# DEFAULT FLASK CODE
if __name__ == '__main__':
    app.run(debug=True)
    import os

    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
