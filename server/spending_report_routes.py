import json
from datetime import datetime, date, time, timedelta

from flask import Blueprint, request, redirect, url_for, jsonify, render_template, make_response, session

from models import db, User, Receipt

spending_report_routes = Blueprint('spending_report_routes', __name__)

@spending_report_routes.route('/users/<int:user_id>/spending_report')
def spending_report(user_id):

    weekdays = ["Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday", "Sunday"]

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return make_response("User doesnn't exist", 404)

    today = datetime.combine(date.today(), time(23,59,59))
    one_week_ago = one_week_before(today)
    
    weeks_receipts = Receipt.query.filter_by(user_id=user_id).filter(Receipt.date <= today).filter(Receipt.date >= one_week_ago).all()

    # if the user has no receipts from the past week then return an empty json object
    if not weeks_receipts:
        return json.dumps({})

    spending_categories = get_spending_categories(user, weeks_receipts)

    #get the week spends
    daily_spends = []
    range_higher = today
    range_lower = datetime.combine(range_higher.date(), time())
    while range_lower >= one_week_ago:
        days_receipts = Receipt.query.filter_by(user_id=user_id).filter(Receipt.date < range_higher).filter(Receipt.date >= range_lower).all()

        total = 0.0
        for receipt in days_receipts:
            total += receipt.total_transaction

        daily_spends.append({ "date": str(weekdays[range_lower.date().weekday()]), "total_spend": round(total,2) })

        range_higher = range_lower
        range_lower = range_lower - timedelta(days=1)

    return json.dumps({"spending_categories": spending_categories, "daily_spends": daily_spends})

def one_week_before(date):
    one_week_ago_date = (date - timedelta(days=6)).date()
    return datetime.combine(one_week_ago_date, time())

def get_spending_categories(user, weeks_receipts):
    spending_categories = {}

    for receipt in weeks_receipts:
        for item in receipt.purchased_items:
            spending_categories[item.category] = spending_categories.get(item.category,0.0) + item.quantity * item.price_per_item

    return delete_zeroes_and_round(spending_categories)

def delete_zeroes_and_round(spending_categories):
    for key in spending_categories.keys():
        if spending_categories[key] == 0:
            del spending_categories[key]
        else:
            spending_categories[key] = round(spending_categories[key], 2)

    return spending_categories    
