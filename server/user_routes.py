from flask import Blueprint
from models import db, User
import json


user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/users')
def users():
    return json.dumps({"users" : [user.serialize() for user in User.query.all()]})


@user_routes.route('/users/<int:user_id>')
def user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return make_response("User " + str(user_id) + " doesn't exist", 404)
    else:
        return json.dumps({"user" : user.serialize()})