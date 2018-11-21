import os
import json
import uuid 
import hashlib
import pprint
import argparse


from flask import Flask, request, render_template
from flask import session, redirect, url_for, escape
from flask import redirect

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


app = Flask(__name__)
print ("Connecting to firebase database...")
cred = credentials.Certificate("buzzplan-d333f-firebase-adminsdk-jhebg-c6fbec263e.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://buzzplan-d333f.firebaseio.com"})
print ("Done")
    
@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        print('here')
        un = request.form['username']
        pwd= request.form['pwd']
        userInfo = db.reference('userinfo')
        userInfo.child('username').set(un)
        userInfo.child('password').set(pwd)
        
        return redirect(url_for('register'))

    else:
        return render_template("register.html")
    
@app.route('/signin')
def signin():
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
 
