# VIRTUAL HAZARD TOURS
# Written by Christoph Wagner-Gillen, last update: 2020-Jan

#Imports
import os
import time
import requests
from flask_sslify import SSLify
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from flask import Flask, flash, redirect, render_template, request, session, url_for,send_from_directory

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or "klas9durtq68u91kqDMVVupigejv4upSNDFaszt8qepe8xcklqr546800hnvXCg"
sslify = SSLify(app, permanent=True)

#Global variables
tour_file_directory="hazard_tours"
topic=""
command="void"
current_pic=2
previous_pic=1
next_pic=3

#Error Handler
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(410)
@app.errorhandler(500)
def server_error(e):
    return render_template('home.html')

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = ''
login_manager.login_message_category = 'error'

#User class definitions
class User(UserMixin):
    def __init__(self, id):
        self.id = id
    def is_authenticated(self):
        return self.authenticated

# Create user, only one at the moment
user=User(1)

# Callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)

#Favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',mimetype='image/vnd.microsoft.icon')

#Generate list of all files and folder in hazard tour directory
file_list=[]
file_index={}
dir_names= next(os.walk("static/" + tour_file_directory))[1]
for name in dir_names:
    i=0
    files=next(os.walk("static/" + tour_file_directory + "/" + name))[2]
    file_list.append([name, files])
    file_index[name]=len(file_list[i][1])

#Start/Homepage
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', file_list=file_list, tour_file_directory=tour_file_directory)

#Login
@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == 'test':
        user=User(1)
        login_user (user)
        session['logged_in'] = True
        return home()
    else:
        error='Passwort not correct. Please try again.'
        time.sleep (1)
    return render_template('login.html', error=error)

#Logout
@app.route("/logout")
def logout():
    logout_user()
    session['logged_in'] = False
    msg="You have been successfully logged out."
    return render_template('login.html', msg=msg)

#Instuctions
@app.route('/instructions')
@login_required
def instructions():
    return render_template('instructions.html')

#Contact
@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

#Tour
@app.route('/tour/<topic>/<current_pic>/<command>')
@login_required
def tour(topic, current_pic, command):
    for key in file_index:
        if key == topic:
            num_pics = int(file_index[key])-1

    if  command == "stop":
        return render_template('home.html', file_list=file_list, tour_file_directory=tour_file_directory)

    if command == "next":     
        if int(current_pic)+1 > num_pics:
            previous_pic=current_pic
            current_pic=1
            next_pic= current_pic+1
        elif int(current_pic)+1 == num_pics:
            previous_pic=current_pic
            current_pic= num_pics
            next_pic= 1   
        else:
            previous_pic=current_pic
            current_pic=int(current_pic)+1
            next_pic=int(current_pic)+1     

    elif command == "back":
        if int(current_pic)-1 < 1:
            current_pic=num_pics
            previous_pic=int(current_pic)-1
            next_pic=1
        elif int(current_pic)-1 == 1:
            previous_pic=current_pic
            current_pic= 1
            next_pic= int(current_pic)+1   
        else:
            next_pic=current_pic
            current_pic=int(current_pic)-1
            previous_pic=int(current_pic)-1  
    else:
        current_pic=1
        previous_pic=num_pics
        next_pic=2
    return render_template('tour.html', topic=topic, tour_file_directory=tour_file_directory, current_pic=current_pic, previous_pic=previous_pic, next_pic=next_pic, command=command)

if __name__ == '__main__':
    app.run (host='0.0.0.0', debug=True, ssl_context='adhoc')
