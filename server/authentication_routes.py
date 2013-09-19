import json

from flask import Blueprint, request, redirect, url_for, jsonify, render_template, make_response, session

from models import db, User

authentication_routes = Blueprint('authentication_routes',
                            __name__)

@authentication_routes.route('/signup', methods=['POST'])
def signup():
    user_query = User.query.filter_by(email_address=request.json["email_address"]).all()
    if user_query:
        return json.dumps({"error": "Email address taken"})
    else:
        user = User(request.json['email_address'],
                request.json['password'],
                request.json['first_name'],
                request.json['last_name'])

        db.add(user)
        db.commit()

        session['user_id'] = user.id

        return json.dumps({"user": user.serialize()})

@authentication_routes.route('/logout')
def logout():
    session.pop('user_id', None)
    return json.dumps({})   

@authentication_routes.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == "POST" and "email_address" in request.json and "password" in request.json:
        
        query = User.query.filter_by(email_address=request.json["email_address"]).all()

        if not query:
            return json.dumps({})

        user = query[0]
        
        if user.check_password(request.json['password']):
            session['user_id'] = user.id
            return json.dumps({"user": user.serialize()})
        else:
            return json.dumps({})
        
    else:
        # used to check if the user is logged in or not
        if "user_id" in session and User.query.filter_by(id=session["user_id"]).all():
            user = User.query.filter_by(id=session["user_id"]).first()
            return json.dumps({"user": user.serialize()})
        else:
            return json.dumps({})