import json
from datetime import datetime, timedelta

from flask import Blueprint, request, redirect, url_for, jsonify, render_template, make_response, session

from models import db, User, Receipt, SpendingCategory, PurchasedItem


spending_category_routes = Blueprint('spending_category_routes', __name__)

@spending_category_routes.route('/users/<int:user_id>/spending_categories', methods=["GET", "POST"])
def spending_categories(user_id):
  user = User.query.filter_by(id=user_id).first()

  if not user:
    return make_response("User doesn't exist", 404)

  if request.method == "GET":
    return json.dumps([sc.serialize() for sc in user.spending_categories])

  else:
    if "category_name" not in request.json or "monthly_allowance" not in request.json:
      return make_response("Need the category_name n monthly_allowance", 400)

    else:
      sc = SpendingCategory(request.json["category_name"], request.json["monthly_allowance"])

      user.spending_categories.append(sc)

      db.add(sc)
      db.commit()

      return json.dumps(sc.serialize())

@spending_category_routes.route('/users/<int:user_id>/spending_categories/<int:sc_id>', methods=["GET", "PUT", "DELETE"])
def spending_category(user_id, sc_id):
  # do the validation of valid sc here
  user = User.query.filter_by(id=user_id).first()
  sc = SpendingCategory.query.filter_by(id=sc_id).first()

  if (not user) or (not sc) or (sc.user != user):
    return make_response("User or card doesn't exist or card doesn't belong to user", 404)

  if request.method == "GET":
    return json.dumps(sc.serialize())

  if request.method == "PUT":
    return spending_category_put(sc)

  if request.method == "DELETE":
    db.delete(sc)
    db.commit()

    return json.dumps({})

def spending_category_put(sc):
  print request.json

  if "category_name" in request.json:
    sc.category_name = request.json["category_name"]

  if "monthly_allowance" in request.json:
    sc.monthly_allowance = request.json["monthly_allowance"]

  db.add(sc)
  db.commit()

  return json.dumps(sc.serialize())

@spending_category_routes.route('/users/<int:user_id>/budgeting_report')
def budgeting_report(user_id):
  # ensure that that user id is a legit one
  user = User.query.filter_by(id=user_id).first()

  if not user:
    return make_response("User " + str(user_id) + " isn't a valid user", 404)

  # Get the params for the budgeting report.
  # By default take this month this year as it is the one the user 
  #   is most likely interested in
  month, year = get_budgeting_time_frame()
  print "month: " + str(month) + " year: "+ str(year)

  receipts = get_receipts_for_month(user, month, year)

  string_cats = {}

  for receipt in receipts:
    for item in receipt.purchased_items:
      string_cats[item.category] = string_cats.get(item.category, 0) + (item.price_per_item * item.quantity)

  print string_cats

  spending_categories = user.spending_categories
  for spending_category in spending_categories:
    spending_category.monthly_spend = string_cats.get(spending_category.category_name, 0.0)
    if spending_category.category_name in string_cats:
      del string_cats[spending_category.category_name]

  remainder = 0.0
  for key in string_cats.keys():
    remainder += string_cats[key]

  remainder = round(remainder, 2)

  return json.dumps({"spending_categories": [sc.serialize() for sc in spending_categories], "other": remainder})

def get_budgeting_time_frame():
  now = datetime.now()
  default_month = now.month
  default_year = now.year

  budgeting_month = int(request.args.get('month', default_month))
  budgeting_year = int(request.args.get('year', default_year))

  return (budgeting_month, budgeting_year)

def get_receipts_for_month(user, month, year):
  start_of_month = datetime(year=year, month=month, day=1)

  next_month = (month%12) + 1
  # if we rolled over from dec to jan then increment year
  if next_month < month:
    year += 1

  end_of_month = datetime(year=year, month=next_month, day=1) - timedelta(microseconds=1)

  return Receipt.query.filter_by(user_id=user.id).filter(Receipt.date>=start_of_month).filter(Receipt.date<=end_of_month).all()  

