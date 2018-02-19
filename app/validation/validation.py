from flask import jsonify
import datetime
import re

def validate_date(date_text):
    date_is_ok = True
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        date_is_ok = False
    return date_is_ok

def validate_ports(ports):
    # We prepare regex one of two possible solution
    if len(ports) <= 5:
        regex = r"([A-Z]+)"
    else:
        regex = r"([a-z_]+)"
    # We do some basic regex and check if text is ok
    match = re.search(regex, ports)

    if match is not None:
       size_regex = match.span()[1]
       size_text = len(ports)
       text_regex = match.group(0)
    else:
        return False

    if text_regex != ports or size_regex != size_text:
        return False

    return True

#def do_some_checks(date_from, date_to, origin, destination,price):
#    BAD_REQUEST = 400


def do_some_checks(date_from, date_to, origin, destination):
   BAD_REQUEST = 400
   # Check dates
   if not validate_date(date_from):
       error_response = jsonify({'Error':'date_from not valid format YYYY-MM-DD'})
       error_response.status_code = BAD_REQUEST
       return error_response

   if not validate_date(date_to):
       error_response = jsonify({'Error':'date_to not valid format YYYY-MM-DD'})
       error_response.status_code = BAD_REQUEST
       return error_response
   if not date_from <= date_to:
       error_response = jsonify({'Error': 'date_to is higher then date_from'})
       error_response.status_code = BAD_REQUEST
       return error_response
   # Check origin
   if not validate_ports(origin):
       error_response = jsonify({'Error': 'origin is not valid format'})
       error_response.status_code = BAD_REQUEST
       return error_response

   # Check destination
   if not validate_ports(destination):
       error_response = jsonify({'Error': 'destination is not valid format'})
       error_response.status_code = BAD_REQUEST
       return error_response

   return '{}'
