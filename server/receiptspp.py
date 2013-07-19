import json, itertools
from datetime import datetime, timedelta, time, date

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
        item.category = request.json["category"]
        db.add(item)
        db.commit()
        return json.dumps({'item': item.serialize()})
    else:
        return make_response("Need category in the JSON", 404)


@app.route('/users/<int:user_id>/spending_report')
def spending_report(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return make_response("User doesnn't exist", 404)

    # get the params from the url
    today = datetime.combine(date.today(), time(23,59,59))
    one_week_ago_date = (today - timedelta(days=6)).date()
    one_week_ago = datetime.combine(one_week_ago_date, time())

    #get the categories
    spending_categories = {}
    for category in user.spending_categories:
        spending_categories[category.category_name] = 0

    # get the amount spent for each category
    weeks_receipts = Receipt.query.filter_by(user_id=user_id).filter(Receipt.date <= today).filter(Receipt.date >= one_week_ago).all()

    # nasty pls fiz
    if not weeks_receipts:
        return json.dumps({})

    for receipt in weeks_receipts:
        for item in receipt.purchased_items:
            spending_categories[item.category] += item.quantity * item.price_per_unit

    for key in spending_categories.keys():
        if spending_categories[key] == 0:
            del spending_categories[key]
        else:
         spending_categories[key] = round(spending_categories[key], 2)

    #get the week spends
    daily_spends = []
    range_higher = today
    range_lower = datetime.combine(range_higher.date(), time())
    while range_lower >= one_week_ago:
        days_receipts = Receipt.query.filter_by(user_id=user_id).filter(Receipt.date < range_higher).filter(Receipt.date >= range_lower).all()

        total = 0.0
        for receipt in days_receipts:
            total += receipt.total_transaction

        daily_spends.append({ "date": str(range_lower.date()), "total_spend": round(total,2) })

        range_higher = range_lower
        range_lower = range_lower - timedelta(days=1)

    return json.dumps({"spending_categories": spending_categories, "daily_spends": daily_spends})

@app.route('/users/<int:user_id>/spending_categories', methods=["GET", "POST"])
def spending_categories(user_id):
    if request.method == "POST":
        time_now = datetime.now()
        one_week_ago = time_now-timedelta(weeks=1)
        time_now = time_now.strftime("%Y/%m/%d %H:%M:%S")
        one_week_ago = one_week_ago.strftime("%Y/%m/%d %H:%M:%S")

        return spending_categories_post(user_id, 
            request.args.get('start', time_now), 
            request.args.get('end', one_week_ago))
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
        return make_response("Hey that's not a real guy, sorry", 404)

# YOU ARE CURRENTLY WORKING HERE
def spending_categories_get(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return json.dumps({ "categories" : [cat.serialize() for cat in user.spending_categories]})
    else:
         return make_response("404 coming your way", 404)
