import json

from flask import Blueprint, request, redirect, url_for, jsonify, render_template, make_response, session
from datetime import datetime, date, time
from sqlalchemy import desc

from models import db, User, Receipt, SpendingCategory, PurchasedItem

receipt_routes = Blueprint('receipt_routes', __name__)

# GET - Gets all of the receipts for the given user
# POST - Creates a new receipt for the given user.
#      - Returns that receipt in JSON form
@receipt_routes.route('/users/<int:user_id>/receipts', methods=['GET','POST'])
def receipts(user_id):
    
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return make_response("User " + str(user_id) + " doesn't exist", 404)

    if request.method == "POST":        
        if validate_request_receipt():
            receipt_date = date_string_to_datetime(request.json["date_time"])

            receipt = Receipt(request.json["store_name"],
                        request.json["category"],
                        request.json["total_transaction"],
                        receipt_date)

            user.receipts.append(receipt)

            if not SpendingCategory.query.filter_by(user_id=user.id).filter_by(category_name=receipt.category).first():
                user.spending_categories.append(SpendingCategory(receipt.category))

            for item in request.json["items"]:
                if validate_item(item):
                    item = PurchasedItem(item["name"],
                        request.json["category"],
                        item["price_per_item"],
                        item["quantity"])

                    receipt.purchased_items.append(item)

            db.add(receipt)
            db.commit()

            return json.dumps({"receipt": receipt.serialize()})

    else: #request is a get and return the receipts of the user
        return get_user_receipts(user)

def validate_item(item):
    return "name" in item and \
        "price_per_item" in item and \
        "quantity" in item

def date_string_to_datetime(date_string):
    date, time = date_string.split(" ")
    day, month, year = [int(x) for x in date.split("/")]
    hour, minute, second = [int(x) for x in time.split(":")]

    receipt_date = datetime(year, month, day, hour, minute, second)

def validate_request_receipt():
    return "store_name" in request.json and \
    "total_transaction" in request.json and \
    "category" in request.json and \
    "date_time" in request.json and \
    "items" in request.json and \
    request.json["items"]

def get_user_receipts(user):
    limit = int(request.args.get('limit', 10000))
    offset = int(request.args.get('offset', 0))
    return json.dumps({ "receipts" : \
            [r.serialize() for r in Receipt.query
            .filter_by(user_id = user.id)
            .order_by(desc(Receipt.date))
            .offset(offset)
            .limit(limit) ]})


# GET - Gets the single receipt AND all its items as JSON
# POST - Nothing (Route not used)
# PUT (NOT YET IMPLEMENTED) - updates it (will be eventually used for sharing categorizing etc)        
# DELETE (NOT YET IMPLEMENTED) - deletes it from the database
@receipt_routes.route('/users/<int:user_id>/receipts/<int:receipt_id>', methods=['GET'])
def receipt(user_id, receipt_id):
    user = User.query.filter_by(id=user_id).first()
    receipt = Receipt.query.filter_by(id=receipt_id).first()

    if not user or not receipt or not user == receipt.user:
        return make_response("404 coming your way", 404)

    return json.dumps({"receipt" : receipt.serialize_with_items()})


