import random, os, requests, json, datetime, time

from flask import Flask, Response, render_template
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
random_numbers = MongoClient('127.0.0.1', 27017).demo.random_numbers


main_response = requests.get('https://api.github.com/search/repositories?&q=opensource&type=Repositories')
# link = main_response.headers.get('link', None)
# if link is not None:
#     print(link)
main_file = main_response.json()
print(main_file)
client = MongoClient('mongodb://localhost:27017/')
database = client['repositories']
collection = database['repositories_collection']
collection.delete_many({})# clean memory
collection.insert_one(main_file)
items = collection.find({}).distinct("items")
print(items)


# speedfield.find({}).forEach(doc)
# collection.update('$set': {'speed':sp})
speed_database = client['speed_field']
speed_collection = speed_database['speed_field_collection']
speed_collection.delete_many({})


language = ["Java", "Ruby"]
max_forks_count = 187
max_commits = 541
max_star = 376
max_contributors = 100
max_size = 10000
max_speed = 200
id = 3788366

lang_database = client['true_lang']
lang_collection = lang_database['true_lang_collection']
lang_collection.delete_many({})#clean memory
lang_collection.insert_many(items)


created_at = lang_collection.distinct('created_at')
print(created_at)
updated_at = lang_collection.distinct('updated_at')
print(updated_at)
size = lang_collection.distinct('size')
print(size)
print("///////////speed///////////////")

print(created_at[0])
year = ""
first_date = []
i = 0
for item in range(len(created_at)):
    year = str(created_at[item][0]) + str(created_at[item][1]) + str(created_at[item][2]) + str(created_at[item][3])
    # date = str(date) + str(a)
    # print(year)
    mon = str(created_at[item][5]) + str(created_at[item][6])
    if created_at[item][5] == '0':
        mon = str(created_at[item][6])
    # print(mon)
    day = str(created_at[item][8]) + str(created_at[item][9])
    if created_at[item][8] == '0':
        day = str(created_at[item][9])
    # print(day)
    date_created_at = int(year) * 360 + int(mon) * 30 + int(day)
    first_date.insert(i, date_created_at)
    i = i + 1
    print(date_created_at)
print(first_date)

print(updated_at[0])
# year = ""
second_date = []
n = 0
for item in range(len(updated_at)):
    year = str(updated_at[item][0]) + str(updated_at[item][1]) + str(updated_at[item][2]) + str(updated_at[item][3])
    mon = str(updated_at[item][5]) + str(updated_at[item][6])
    if updated_at[item][5] == '0':
        mon = str(updated_at[item][6])
    day = str(updated_at[item][8]) + str(updated_at[item][9])
    if updated_at[item][8] == '0':
        day = str(updated_at[item][9])
    date_updated_at = int(year) * 360 + int(mon) * 30 + int(day)
    second_date.insert(n, date_updated_at)
    n = n + 1
    print(date_updated_at)
print(first_date)
for item in range(len(created_at)):
    lang_collection.update_one({
        'created_at': created_at[item],
        'updated_at': updated_at[item]},
        {'$set': {'speed': size[item]/(second_date[item] - first_date[item])}})
sp = lang_collection.find({}, {'_id': 0, 'created_at': 1, 'updated_at': 1, 'size': 1, 'speed': 1})
for sp_item in sp:
    print(sp_item)


task1 = lang_collection.find({'language': {'$in': language},
                              'forks': {'$lte': max_forks_count},
                              'stargazers_count': {'$lte': max_star},
                              'size': {'$lte': max_size},
                              'speed': {'$lte': max_speed}},
                             {'id': 1,
                              'name': 1,
                              'language': 1,
                              'forks': 1,
                              'stargazers_count': 1,
                              'size': 1,
                              'speed': 1}) #cursor - выборка
print("Java language")
for ind in task1:
    print(ind)




# for item in forks:
#     sp = lang_collection.aggregate([{'$project': {'speed': {'$subtract': [forks[0], 0]}}}])
#     for sp_item in sp:
#         print(sp_item)


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
    return render_template('index-basic.html')

    #return Response(json.dumps(extracted, default=json_util.default), status=200, mimetype='application/json')
    #last_numbers = list(random_numbers.find({"_id" : "lasts"}))
    #extracted = [d['value'] for d in last_numbers[0]['items']]

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.config['DEBUG'] = True
    app.run(host='127.0.0.1', port=port)
