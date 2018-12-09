import random, os, requests, json, datetime, time

from flask import Flask, Response, render_template
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
random_numbers = MongoClient('127.0.0.1', 27017).demo.random_numbers

main_response = requests.get('https://api.github.com/search/repositories?q=github&type=Repositories')
main_file = main_response.json()
print(main_file)
client = MongoClient('mongodb://localhost:27017/')
database = client['repositories']
collection = database['repositories_collection']
collection.delete_many({})# clean memory
collection.insert_one(main_file)
items = collection.find({}).distinct("items")
print(items)

language = "Java"

lang_database = client['true_lang']
lang_collection = lang_database['true_lang_collection']
lang_collection.delete_many({})#clean memory
lang_collection.insert_many(items)
task1 = lang_collection.find({'language': language}).limit(1000) #cursor - выборка
print("Java language")
for ind in task1:
    print(ind)


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
