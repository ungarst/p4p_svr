import json
from datetime import datetime

from flask import request, redirect, url_for, jsonify, render_template, make_response, session
from sqlalchemy import desc

from server import app
from models import db, User, Receipt, PurchasedItem, SpendingCategory

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

@app.route('/users/<int:user_id>')
def user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return make_response("User " + str(user_id) + " doesn't exist", 404)
    else:
        return json.dumps({"user" : user.serialize()})


# GET - Gets all of the receipts for the given user
# POST - Creates a new receipt for the given user.
#      - Returns that receipt in JSON form
@app.route('/users/<int:user_id>/receipts', methods=['GET','POST'])
def receipts(user_id):
    
    user = User.query.filter_by(id=user_id).first()

    if not user:
            return make_response("User " + str(user_id) + " doesn't exist", 404)

    # everything in this needs some mad error prevention
    if request.method == "POST":
        
        if "storeName" in request.json and \
            "taxRate" in request.json and \
            "totalTransaction" in request.json and \
            "category" in request.json and \
            "dateTime" in request.json and \
            "items" in request.json and \
            request.json["items"]:

            date, time = request.json["dateTime"].split(" ")
            day, month, year = [int(x) for x in date.split("/")]
            hour, minute, second = [int(x) for x in time.split(":")]

            receipt_date = datetime(year, month, day, hour, minute, second)

            receipt = Receipt(request.json["storeName"],
                        request.json["category"],
                        request.json["taxRate"],
                        request.json["totalTransaction"],
                        receipt_date)

            user.receipts.append(receipt)

            if not SpendingCategory.query.filter_by(user_id=user.id).filter_by(category_name=receipt.category).first():
                user.spending_categories.append(SpendingCategory(receipt.category))

            # This for loop especially needs it
            for item in request.json["items"]:
                item = PurchasedItem(item["item"]["title"],
                    request.json["category"],
                    item["item"]["price"],
                    item["itemQuantity"])

                receipt.purchased_items.append(item)

            db.add(receipt)
            db.commit()

            return json.dumps({"receipt": receipt.serialize()})

        else:
            print request.json
            if "storeName" in request.json:
                print "storeName here"
            if "taxRate" in request.json:
                print "taxRate here"
            if "totalTransaction" in request.json:
                print "totalTransaction here"
            if "category" in request.json:
                print "category here" 
            if "dateTime" in request.json:
                print "date here"
            if "items" in request.json:
                print "items here"
            return make_response('Incorrect data in json', 400)

    else: #request is a get and return all the receipts of the user
        return json.dumps({"receipts" : [r.serialize() for r in user.receipts]})



# GET - Gets the single receipt AND all its items as JSON
# POST - Nothing (Route not used)
# PUT (NOT YET IMPLEMENTED) - updates it (will be eventually used for sharing categorizing etc)        
# DELETE (NOT YET IMPLEMENTED) - deletes it from the database
@app.route('/users/<int:user_id>/receipts/<int:receipt_id>', methods=['GET'])
def receipt(user_id, receipt_id):
    user = User.query.filter_by(id=user_id).first()
    receipt = Receipt.query.filter_by(id=receipt_id).first()

    if not user or not receipt or not user == receipt.user:
        return make_response("404 coming your way", 404)

    return json.dumps({"receipt" : receipt.serialize_with_items()})
    # Get the receipt
    # Check the user of the receipt is the same as the user

    # return the serialized with items 

@app.route('/users/<int:user_id>/receipts/<int:receipt_id>/purchased_items/<int:item_id>', methods=['PUT'])
def item(user_id, receipt_id, item_id):
    # perform some sort of validation to ensure that the item belongs to that receipt and that user

    item = PurchasedItem.query.filter_by(id=item_id).first()

    if not item:
        return make_response("This item doesn't exist", 404)

    receipt = item.receipt
    if receipt.id != receipt_id:
        return make_response("This item doesn't belong to the receipt specified", 404)

    user = receipt.user
    if user.id != user_id:
        return make_response("The item doesn't belong to the user specified", 404)


    if "category" in request.json:
        print "her"
        item.category = request.json["category"]
        db.add(item)
        db.commit()
        return json.dumps({'item': item.serialize()})
    else:
        return make_response("Need category in the JSON", 404)
    return "hello world"


@app.route('/users/<int:user_id>/spending_categories', methods=["GET", "POST"])
def spending_categories(user_id):
    if request.method == "POST":
        return spending_categories_post(user_id, request.json)
    elif request.method == "GET":
        return spending_categories_get(user_id)

def spending_categories_post(user_id, data):
    user = User.query.filter_by(id=user_id).first()
    if user:
        try:
            category = SpendingCategory(data["category_name"])
        except KeyError:
            return make_response("404 coming your way", 404)

        user.spending_categories.append(category)
        db.add(user)
        db.commit()

        return json.dumps({"category" : category.serialize()})
    
    else: 
        return make_response("404 coming your way", 404)


def spending_categories_get(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return json.dumps({ "categories" : [cat.serialize() for cat in user.spending_categories]})
    else:
         return make_response("404 coming your way", 404)
