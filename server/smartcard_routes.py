import json

from flask import Blueprint, request, redirect, url_for, jsonify, render_template, make_response, session

from models import db, User, Receipt, SpendingCategory, PurchasedItem, Smartcard

smartcard_routes = Blueprint('smartcard_routes', __name__)


# POST - create a new card for the user
# PUT - {enabled: true/false}
# GET - return their card 
# DELETE - remove their card
@smartcard_routes.route('/users/<int:user_id>/smartcard', methods=["GET", "POST", "PUT", "DELETE"])
def smartcard(user_id):
	user = User.query.filter_by(id=user_id).first()
	if not user:
		return make_response("USER " + str(user_id) + " DOESN'T EXIST", 404)

	if request.method == "GET":
		if user.smartcard:
			return json.dumps(user.smartcard.serialize())
		else:
			return make_response("User " + str(user_id) + " has no smartcard", 404)

	elif request.method == "POST":
		return new_smartcard(user)

	elif request.method == "PUT":
		return update_smartcard_status(user.smartcard)

	elif request.method == "DELETE":
		sc = user.smartcard
		db.delete(sc)
		db.commit()

		return json.dumps({})

def new_smartcard(user):
	if validate_smartcard():
		user.smartcard = Smartcard(request.json["smartcard_number"], request.json["enabled"])
		db.add(user)
		db.commit()
		return json.dumps(user.smartcard.serialize())

	else:
		return make_response("Incorrect data in JSON", 400)

def validate_smartcard():
	return "smartcard_number" in request.json and "enabled" in request.json

def update_smartcard_status(smartcard):
	if not "enabled" in request.json:
		return make_response("Incorrect data in json", 400)

	smartcard.enabled = request.json["enabled"]
	db.add(smartcard)
	db.commit()

	return json.dumps(smartcard.serialize())


#GET - Return the user who owns the card
@smartcard_routes.route("/user_from_smartcard/<smartcard_number>", methods=["GET"])
def get_user_from_smartcard(smartcard_number):
	card_owner = Smartcard.query.filter_by(smartcard_number=smartcard_number).first().user
	if card_owner:
		return json.dumps(card_owner.serialize())
	else:
		return make_response("CARD DOENSN'T EXIST", 400)

