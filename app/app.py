from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException, default_exceptions

import sys
import os
import psycopg2
import time

from validation.validation import do_some_checks
from postgresql.postgresql import search_price, insert_records



app = Flask(__name__)

DB_USER = 'postgres'
DB_PASS = ''
DB_NAME = 'postgres'
DB_HOST = 'ratestask'

# IS there postgresql ?
# We going to wait 4 sec for DB to get up.
time.sleep(4)

conn = psycopg2.connect("dbname='{}' user='{}' password='{}' host='{}'".format(DB_NAME, DB_USER, DB_PASS, DB_HOST))
cur = conn.cursor()


# Error handling - we want to have for all HTTP codes json response.
def error_handling(error):
    # We want to be sure that error are member of HTTP
    resp = '{}'
    if isinstance(error, HTTPException):
        resp = jsonify({'Error': error.description}, error.code)
        # We want that our logs have proper error code not 200
        resp.status_code = error.code
    else:
        # If we don't cover code at all - at least we have error message that req is wrong
        resp = jsonify({'Error': 'Something went wrong'}, 500)
        resp.status_code = 500
    return resp


# GET Method  - search for price and date
# POST Method - insert new record
@app.route('/v1/rates/<date_from>/<date_to>/<origin>/<destination>/', methods=['GET'])
def rates(date_from, date_to, origin, destination):
    # We want to have default response if something goes rl bad
    response = '{}'
    # Here we do some checks of input data and if are nor proper we send error message
    try:
        check_input = do_some_checks(date_from, date_to, origin, destination)
    except:
        # Here would error handling to solve report back to client
        print("Unexpected error:", sys.exc_info()[0])
        raise

    if check_input != '{}': return check_input

    response = search_price(cur, date_from, date_to, origin, destination)

    return response

@app.route('/v1/rates/<date_from>/<date_to>/<origin>/<destination>/<int:price>/', methods=['POST'])
def insert_price(date_from, date_to, origin, destination, price):
    response = '{}'
    # Here we do some checks of input data and if are nor proper we send error message
    try:
        check_input = do_some_checks(date_from, date_to, origin, destination)
    except:
        # Here would error handling to solve report back to client
        print("Unexpected error:", sys.exc_info()[0])
        raise

    if check_input != '{}': return check_input

    response = insert_records(cur,conn, date_from, date_to, origin, destination, price)

    return response

if __name__ == '__main__':
    # We want to bind error handling function to all "wrong" requests

    for code in default_exceptions.keys():
        app.register_error_handler(code, error_handling)

    app.run(host='0.0.0.0', port=80)
