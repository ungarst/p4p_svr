import json

from flask import request, redirect, url_for, jsonify, render_template, make_response, session
from sqlalchemy import desc

from server import app
from models import db, User

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def root():
    # serve up the angular
    if 'username' in session:
        return "Signed in as " + session['username']
    return "not signed in"

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        user = User(request.form['username'],
                request.form['password'])

        session['username'] = request.form['username']

        db.add(user)
        db.commit()
        
        return redirect(url_for('root'))

    else:
        return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('root'))   

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST" and "username" in request.form and "password" in request.form:
        query = User.query.filter_by(username=request.form["username"]).all()

        if not query:
            return "no users with that name"

        user = query[0]
        if user.check_password(request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('root'))
        else:
            return "wrong pw"
        


    return render_template('login.html')
    #check the password
    #if good then set the cookie
    #redirect

@app.route('/users')
def users():
    return json.dumps([user.serialize() for user in User.query.all()])


@app.route('/jsonmirror', methods=['GET', 'POST'])
def mirror():
    return json.dumps(request.form)