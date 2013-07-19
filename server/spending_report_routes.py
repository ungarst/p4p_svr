import json
from datetime import datetime, date, time, combine

from flask import Blueprint

from models import db, User, Receipt

@spending_report_routes.route('/users/<int:user_id>/spending_report')
def spending_report(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return make_response("User doesnn't exist", 404)

    today = datetime.combine(date.today(), time(23,59,59))
    one_week_ago = one_week_ago
    
    weeks_receipts = Receipt.query.filter_by(user_id=user_id).filter(Receipt.date <= today).filter(Receipt.date >= one_week_ago).all()

    # if the user has no receipts from the past week then return an empty json object
    if not weeks_receipts:
        return json.dumps({})

    spending_categories = spending_categories(user, weeks_receipts)

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

def one_week_ago():
    one_week_ago_date = (today - timedelta(days=6)).date()
    return combine(one_week_ago_date, time())

def spending_categories(user, weeks_receipts):
    spending_categories = zeroed_spending_categories(user)

    for receipt in weeks_receipts:
        for item in receipt.purchased_items:
            spending_categories[item.category] += item.quantity * item.price_per_unit

    return delete_zeroes_and_round(spending_categories)

def delete_zeroes_and_round(spending_categories):
    for key in spending_categories.keys():
        if spending_categories[key] == 0:
            del spending_categories[key]
        else:
            spending_categories[key] = round(spending_categories[key], 2)

    return spending_categories    

def zeroed_spending_categories(user):
    spending_categories = {}
    for category in user.spending_categories:
        spending_categories[category.category_name] = 0

    return spending_categories