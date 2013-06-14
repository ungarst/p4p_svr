import json

from flask import request, redirect, url_for, jsonify, render_template, make_response
from sqlalchemy import desc

from server import app
from models import db, User


@app.route('/')
def root():
    # serve up the angular
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == "POST":
		user = User(request.form['nick'],
				request.form['email'],
				request.form['password'])
		db.add(user)
		db.commit()
		response = json.dumps([
			p.serialize() for p in User.query.all()])
		return response
	else:
		return render_template('signup.html')

