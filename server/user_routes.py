import json

from flask import Blueprint, request, redirect, url_for, jsonify, render_template, make_response, session

from models import db, User

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users')
def users():
    return json.dumps({"users" : [user.serialize() for user in User.query.all()]})


@user_routes.route('/users/<int:user_id>', methods=["GET", "PUT"])
def user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return make_response("User " + str(user_id) + " doesn't exist", 404)
    
    if request.method == "GET":
        return json.dumps({"user" : user.serialize()})
    elif request.method == "PUT":
    	return user_put(user)

def user_put(user):
	for key in request.json.keys():
		if key == "id":
			pass
		elif hasattr(user, key):
			setattr(user, key, request.json[key])

	user.generate_gravatar_url()

	db.add(user)
	db.commit()

	return json.dumps({"user": user.serialize()})
