#!/usr/bin/env python
import os

from flask import Flask

from models import db

app = Flask(__name__)

app.config.update(
    DEBUG=False if "PRODUCTION" in os.environ else True,
)


@app.teardown_request
def shutdown_session(exception=None):
    db.remove()

import server.receiptspp
