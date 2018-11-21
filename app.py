import os
import json
import uuid 
import hashlib
import pprint
import argparse


from flask import Flask, request, render_template
from flask import session, redirect, url_for, escape
from flask import redirect
from flask import flash

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
        un = request.form['username']
        pwd= request.form['pwd']
        print(un)
        userInfo = db.reference('userinfo')
        hashID =abs(hash(un))
        userInfo.child('ID').set(str(hashID))
        ID = db.reference('ID')
        ID.child('username').set(un)
        ID.child('password').set(pwd)
        flash('You were successfully registered')
        return render_template('index.html')
        #return redirect(url_for('register'))

    else:
        return render_template("register.html")
    
@app.route('/signin',  methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        un = request.form['username']
        pwd= request.form['pwd']
        userInfo = db.reference('userinfo')
        hashID =abs(hash(un))
        if userInfo.child('ID').get(hashID):
            print(un)
        else:
            print("No")
        #ID = db.reference('ID')
        #ID.child('username').get(un)
        #ID.child('password').get(pwd)

    else:
        return render_template('signin.html')

if __name__ == '__main__':
    #app.secret_key = 'super secret key'
    #app.config['SESSION_TYPE'] = 'filesystem'
    
    app.run(debug=True, use_reloader=True)
 
