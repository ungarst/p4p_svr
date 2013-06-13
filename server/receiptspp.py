import json

from flask import request, redirect, url_for, jsonify, render_template, make_response
from sqlalchemy import desc

from server import app
#from models import db, Patient, VitalInfo, Department


@app.route('/')
def root():
    # serve up the angular
    return render_template('index.html')

