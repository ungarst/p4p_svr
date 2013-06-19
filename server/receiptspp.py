import json

from flask import request, redirect, url_for, jsonify, render_template, make_response, session
from sqlalchemy import desc

from server import app
from models import db, User, Receipt

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def root():
    # serve up the angular
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == "POST":
        user = User(request.json['email_address'],
                request.json['password'],
                request.json['first_name'],
                request.json['last_name'])

        db.add(user)
        db.commit()

        session['user_id'] = user.id

        return json.dumps({"user": user.serialize()})

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return json.dumps({})   

@app.route('/login', methods=['GET', 'POST'])
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


@app.route('/users')
def users():
    return json.dumps({"users" : [user.serialize() for user in User.query.all()]})


@app.route('/jsonmirror', methods=['GET', 'POST'])
def mirror():
    return json.dumps(request.json)

@app.route('/receipts', methods=['GET', 'POST']) 
def receipts():
    if request.method == "GET":
        query = Receipt.query.all()

        return json.dumps([r.serialize() for r in query])

    else:
        if "store_name" in request.json and \
            "tax_rate" in request.json and \
            "total_transaction" in request.json:

            receipt = Receipt(request.json["store_name"],
                    request.json["tax_rate"],
                    request.json["total_transaction"])

            db.add(receipt)
            db.commit()

            return json.dumps({"receipt": receipt.serialize()})

        else:
            return "Bad request"



