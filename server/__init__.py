#!/usr/bin/env python
import os

from flask import Flask

# Blueprints
from server.user_routes import user_routes
from server.receipt_routes import receipt_routes

from models import db

app = Flask(__name__)

# Register Blueprints that were imported above
app.register_blueprint(user_routes)
app.register_blueprint(receipt_routes)

app.config.update(
    DEBUG=False if "PRODUCTION" in os.environ else True,
)


@app.teardown_request
def shutdown_session(exception=None):
    db.remove()

import server.receiptspp
