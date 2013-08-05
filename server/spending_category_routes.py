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
		return spending_categories_get(user)

	else:
		if "category_name" not in request.json:
			return make_response("Need the category_name", 400)

		else:
			sc = SpendingCategory(request.json["spending_category"])
			if "monthly_allowance" in request.json:
				sc.monthly_allowance = request.json["monthly_allowance"]

			users.spending_categories.append(sc)

			db.add(sc)
			db.commit()

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
		sb.delete(sc)
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

def spending_categories_get(user):
	# get applicable receipts
	d = datetime.now()
	som = d - timedelta(days=d.day-1, hours=d.hour, minutes=d.minute, seconds=d.second, microseconds=d.microsecond)
	receipts = Receipt.query.filter_by(user_id=user.id).filter(Receipt.date >= som).all()

	cats = {}

	for receipt in receipts:
		for item in receipt.purchased_items:
			cats[item.category] = cats.get(item.category, 0) + (item.price_per_item * item.quantity)

	spending_categories = user.spending_categories
	for spending_category in spending_categories:
		spending_category.monthly_spend = cats.get(spending_category.category_name, 0.0)

	return json.dumps([sc.serialize() for sc in spending_categories])

