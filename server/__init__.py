#!/usr/bin/env python
import os

from flask import Flask, render_template

# Blueprints
from server.user_routes import user_routes
from server.receipt_routes import receipt_routes
from server.spending_report_routes import spending_report_routes
from server.purchased_item_routes import purchased_item_routes
from server.authentication_routes import authentication_routes
from server.smartcard_routes import smartcard_routes


from models import db

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
def root():
    # serve up the angular
    return render_template('index.html')

# Register Blueprints that were imported above
app.register_blueprint(user_routes)
app.register_blueprint(receipt_routes)
app.register_blueprint(spending_report_routes)
app.register_blueprint(purchased_item_routes)
app.register_blueprint(authentication_routes)
app.register_blueprint(smartcard_routes)



app.config.update(
    DEBUG=False if "PRODUCTION" in os.environ else True,
)


@app.teardown_request
def shutdown_session(exception=None):
    db.remove()
