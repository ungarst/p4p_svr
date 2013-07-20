import json

from flask import Blueprint, request, redirect, url_for, jsonify, render_template, make_response, session

from models import db, PurchasedItem, Receipt, User

purchased_item_routes = Blueprint('purchased_item_routes', __name__)

@purchased_item_routes.route('/users/<int:user_id>/receipts/<int:receipt_id>/purchased_items/<int:item_id>', methods=['PUT'])
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