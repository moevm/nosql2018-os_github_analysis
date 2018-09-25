import random, os, json, datetime, time

from flask import Flask, Response, render_template
from pymongo import MongoClient
from bson import json_util


app = Flask(__name__)
random_numbers = MongoClient('127.0.0.1', 27017).demo.random_numbers

@app.route("/add/<int:lower>/<int:upper>")
def random_generator(lower, upper):
    number = str(random.randint(lower, upper))
    random_numbers.update(
        {"_id" : "lasts"},
        {"$push" : {
            "items" : {
                "$each": [{"value" : number, "date": datetime.datetime.utcnow()}],
                "$sort" : {"date" : -1},
                "$slice" : 5
            }
        }},
        upsert=True
    )

    return Response(number, status=200, mimetype='application/json')


@app.route("/")
def last_number_list():
    return render_template('index.html')

    #return Response(json.dumps(extracted, default=json_util.default), status=200, mimetype='application/json')
    #last_numbers = list(random_numbers.find({"_id" : "lasts"}))
    #extracted = [d['value'] for d in last_numbers[0]['items']]

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.config['DEBUG'] = True
    app.run(host='127.0.0.1', port=port)