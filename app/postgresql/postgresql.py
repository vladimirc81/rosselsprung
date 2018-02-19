import psycopg2
import json
from datetime import date, timedelta
from flask import jsonify

def generate_date(date_from, date_to):
    year_from, month_from, day_from = (int(s) for s in date_from.split('-'))
    year_to, month_to, day_to = (int(s) for s in date_to.split('-'))

    date_from_class = date(year_from, month_from, day_from)  # start date
    date_to_class = date(year_to, month_to, day_to)  # end date

    delta = date_to_class - date_from_class  # timedelta
    list_of_days = list()

    for i in range(delta.days + 1):
        list_of_days.append(str(date_from_class + timedelta(days=i)))


    return list_of_days

def insert_records(cur,conn, date_from, date_to, origin, destination,price):
    BAD_REQUEST = 400
    # explain analyze select code from ports where code='IEORK' or code='CNNBO' limit 2 ;
    # explain analyze select code from ports where code='IEORK' or code='CNNBO' ;
    # To see diff
    cur.execute("select code from ports where code=(%s) or code=(%s) limit 2;", (origin, destination))
    max_code_exist = cur.fetchall()

    if len(max_code_exist) != 2:
        error_response = jsonify({"Error": "One of port does not exist"})
        error_response.status_code = BAD_REQUEST
        return error_response

    for day in generate_date(date_from,date_to):
        cur.execute("insert into prices (orig_code, dest_code, day, price) values (%s, %s, %s, %s);", (origin, destination,day,price))

    conn.commit()

    return jsonify({"Ok":"Ok"})

def search_price(cur,date_from, date_to, origin, destination):

    list_days = generate_date(date_from, date_to)

    results_sql_query = dict()
    sql_query = "select avg(price) from prices where day=%s and "
    if len(origin) != 5:
       sql_query = sql_query + " orig_code in (select code from ports where parent_slug=%s) and "
    else:
       sql_query = sql_query + " orig_code=%s and "

    if len(destination) != 5:
        sql_query = sql_query + " dest_code in (select code from ports where parent_slug=%s) "
    else:
        sql_query = sql_query + " dest_code=%s "

    for day in list_days:
       print(day)
       try:
         cur.execute(sql_query, (day, origin,destination))
       except Exception:
         raise
       # We pick up int instead of float. Why? I guess because of example I have in readme
       price = int(cur.fetchall()[0][0])
       results_sql_query[day] = price
    final_json_results = json.dumps([{"day": str(day), "average_price": price} for day,price in results_sql_query.items()], indent=4)

    return final_json_results
