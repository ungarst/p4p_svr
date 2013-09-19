import json

from flask import Blueprint, request, make_response
from datetime import datetime
from sqlalchemy import desc

from models import db, User, Receipt, PurchasedItem

receipt_routes = Blueprint('receipt_routes', __name__)

# GET - Gets all of the receipts for the given user
#          - If you want only the receipts after a given date then you may provide after_day, after_month and after_year as params
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

            for item in request.json["items"]:
                if validate_item(item):
                    item = PurchasedItem(item["name"],
                        request.json["category"],
                        item["price_per_item"],
                        item["quantity"])

                    receipt.purchased_items.append(item)


            db.add(user)
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

    return datetime(year, month, day, hour, minute, second)

def validate_request_receipt():
    return "store_name" in request.json and \
    "total_transaction" in request.json and \
    "category" in request.json and \
    "date_time" in request.json and \
    "items" in request.json and \
    request.json["items"]

def get_user_receipts(user):
    query = Receipt.query.filter_by(user_id = user.id).order_by(desc(Receipt.date))

    after_date = get_after_date()
    if after_date:
        print after_date
        query = query.filter(Receipt.date >= after_date)

    if 'offset' in request.args:
        query = query.offset(int(request.args['offset']))

    if 'limit' in request.args:      
        query = query.limit(int(request.args['limit']))

    return json.dumps({ "receipts" : \
            [r.serialize() for r in query.all()]})

def get_after_date():
    if date_provided_in_query_params():
        after_day = int(request.args["after_day"])
        after_month = int(request.args["after_month"])
        after_year = int(request.args["after_year"])
        try:
            return datetime(day=after_day, month=after_month,year=after_year)
        except ValueError:
            return None
        
    else:
        return None


def date_provided_in_query_params():
    return "after_day" in request.args and \
        "after_month" in request.args and \
        "after_year" in request.args


# GET - Gets the single receipt AND all its items as JSON
# POST - Nothing (Route not used)
# PUT (NOT YET IMPLEMENTED) - updates it (will be eventually used for sharing categorizing etc)        
# DELETE (NOT YET IMPLEMENTED) - deletes it from the database
@receipt_routes.route('/users/<int:user_id>/receipts/<int:receipt_id>', methods=['GET', 'DELETE'])
def receipt(user_id, receipt_id):
    user = User.query.filter_by(id=user_id).first()
    receipt = Receipt.query.filter_by(id=receipt_id).first()

    if not user or not receipt or not user == receipt.user:
        return make_response("404 coming your way", 404)

    if request.method == "GET":
        return json.dumps({"receipt" : receipt.serialize_with_items()})
    elif request.method == "DELETE":
        db.delete(receipt)
        db.commit()

        return json.dumps({})

@receipt_routes.route('/receipt_size')
def receipt_size():
    return json.dumps({
        "category": "Groceries",
        "store_name": "Countdown Birkenhead",
        "total_transaction": 123.81,
        "receipt_id": 99,
        "date_time": "2013-08-26 15:56:19.770508"
    })


