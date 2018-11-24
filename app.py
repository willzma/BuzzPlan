from flask import Flask, request, render_template
from flask import session, redirect, url_for, escape
from flask import redirect
from flask import flash
from firebase_admin import credentials
from firebase_admin import db
import argparse
import firebase_admin
import hashlib
import json
import os
import pprint
import uuid 


app = Flask(__name__)
cred = credentials.Certificate("buzzplan-d333f-firebase-adminsdk-jhebg-c6fbec263e.json")
firebase_admin.initialize_app(cred, {'databaseURL': "https://buzzplan-d333f.firebaseio.com"})


@app.route('/')
def homepage():
    return render_template('index.html', username='#')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        degree, program, thread = request.form['degree'], request.form['program'], request.form['thread']
        print(username, password, degree, program, thread)
        db.reference('users').child(username).set({
            'username': username,
            'password': password,
            'degree': degree,
            'program': program,
            'thread': thread
        })
        return render_template('index.html', username=username)
    else:
        return render_template("signup.html")


@app.route('/signin',  methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username, password = request.form['username'], request.form['password']
        user = db.reference('users').child(username).get()
        if not user:
            print("User \'{}\' attempted to sign in, but that username doesn't exist!".format(username))
            return render_template('signin.html')
        if password != user['password']:
            print("User \'{}\' attempted to sign in with the wrong password.".format(username))
            return render_template('signin.html')
        session['username'], session['signed-in'] = username, True
        print("User \'{}\' successfully signed in.".format(username))
        return render_template('index.html', username=username)
    else:
        return render_template('signin.html')


if __name__ == '__main__':
    app.secret_key = 'ce04bb09-b83c-4636-95a6-daca7e992717'
    #app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, use_reloader=True)
 
