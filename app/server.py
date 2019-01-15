import random, os, requests, json, datetime, time

from flask import Flask, Response, render_template, url_for, request, jsonify
from pymongo import MongoClient
from bson import json_util

app = Flask(__name__)
random_numbers = MongoClient('127.0.0.1', 27017).demo.random_numbers

#         АНЯ смотри сразу строчку 139

main_response = requests.get('https://api.github.com/search/repositories?&q=opensource&type=Repositories&per_page=100')

main_file = main_response.json()
# print(main_file)

client = MongoClient('mongodb://localhost:27017/')
database = client['repositories']
collection = database['repositories_collection']
collection.delete_many({})# clean memory
collection.insert_one(main_file)
items = collection.find({}).distinct("items")
print(items)
for item in items:
    collection.insert_one(item)
docs = collection.find({})

# speedfield.find({}).forEach(doc)
# collection.update('$set': {'speed':sp})
# speed_database = client['speed_field']
# speed_collection = speed_database['speed_field_collection']
# speed_collection.delete_many({})


language = ["Ruby"]
max_forks_count = 187
max_commits = 541
max_star = 376
max_contributors = 100
max_size = 10000
max_speed = 200
id = 3788366

# calculating field speed
created_at = collection.distinct('created_at')
# print(created_at)
updated_at = collection.distinct('updated_at')
# print(updated_at)
size = collection.distinct('size')
# print(size)
# print("///////////speed///////////////")
#
# print(created_at[0])
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
    # print(date_created_at)
# print(first_date)

# print(updated_at[0])
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
    # print(date_updated_at)
# print(first_date)
for item in range(len(created_at)):
    collection.update_one({
        'created_at': created_at[item],
        'updated_at': updated_at[item]},
        {'$set': {'speed': size[item]/(second_date[item] - first_date[item])}})
sp = collection.find({}, {'_id': 0, 'created_at': 1, 'updated_at': 1, 'size': 1, 'speed': 1})
# for sp_item in sp:
#     print(sp_item)



@app.route("/add/<int:lower>/<int:upper>")
def random_generator(lower, upper):
    number = str(random.randint(lower, upper))
    random_numbers.update(
        {"_id": "lasts"},
        {"$push": {
            "items": {
                "$each": [{"value": number, "date": datetime.datetime.utcnow()}],
                "$sort": {"date": -1},
                "$slice": 5
            }
        }},
        upsert=True
    )

    return Response(number, status=200, mimetype='application/json')

# @app.route("/init/<string:languages>")
# def languages_list(languages):
#     # lang_response = requests.get('http://127.0.0.1:5000/init?language[]=Ruby')
#     # print(lang_response)
#     init_language = [languages]
#     print(init_language)
#     lang_task = collection.find({'language': {'$in': init_language}})
#     print("My init cursor")
#     for index in lang_task:
#         print(index)
#     lang_file = json.dumps({'success':'true'})
#     # response = app.response_class(
#     #     response=json.dumps({'success':'true'}),
#     #     status=200,
#     #     mimetype='application/json'
#     # )
#     # print(response)
#     return Response(lang_file, status=200, mimetype='application/json')

#на этот метод должен прийти массив languages[] (выбранные пользователем языки)
#что здесь происходит: я делаю выборку из изначальной коллекции по языкам, которые пришли от тебя
#переходя по адресу http://127.0.0.1:5000/init?languages[]=Ruby&languages[]=Java произойдёт фильтрация по языкам java и ruby
#на выходе json об успешном выполнении
@app.route("/init", methods=['GET'])
def languages_list():
    languages = request.args.getlist('languages[]')
    print(languages)
    init_database = client.repositories
    init_collection = init_database.repositories_collection
    lang_task = init_collection.find({'language': {'$in': languages}, }, {'_id': 0, 'id': 1,
                              'name': 1,
                              'language': 1,
                              'forks': 1,
                              'stargazers_count': 1,
                              'size': 1,
                              'speed': 1})

    # print("My init cursor")
    # for index in lang_task:
    #     print(index)

    init_db = client['init_languages']
    init_col = init_db['languages_collection']
    init_col.delete_many({})  # clean memory
    for index in lang_task:
        init_col.insert_one(index)
        print(index)
    print(init_col)
    for init_ind in init_col.find({}):
        print(init_ind)

    lang_file = json.dumps({'languages': languages, 'success': 'true'})

    return Response(lang_file, status=200, mimetype='application/json')

#сюда должны прийти параметры фильтрации forksFrom, forksTo и тд
#переходя по адресу http://127.0.0.1:5000/list?forksTo=34&starsFrom=0&starsTo=200&sizeFrom=0&sizeTo=5000&speedFrom=0&speedTo=7
#произойдёт фильтрация
#возвращает json с конечной выборкой значения которой нужно вывести на графики
@app.route("/list", methods = ['GET'])
def filter_list():

    forksFrom = request.args.get('forksFrom')
    if forksFrom is None:
        forksFrom=0
    forksFrom = int(forksFrom)

    forksTo = request.args.get('forksTo')
    if forksTo is None:
        forksTo=9999999
    forksTo = int(forksTo)

    starsFrom = request.args.get('starsFrom')
    if starsFrom is None:
        starsFrom=0
    starsFrom = int(starsFrom)

    starsTo = request.args.get('starsTo')
    if starsTo is None:
        starsTo=9999999
    starsTo = int(starsTo)

    sizeFrom = request.args.get('sizeFrom')
    if sizeFrom is None:
        sizeFrom=0
    sizeFrom = int(sizeFrom)

    sizeTo = request.args.get('sizeTo')
    if sizeTo is None:
        sizeTo=9999999
    sizeTo = int(sizeTo)

    speedFrom = request.args.get('speedFrom')
    if speedFrom is None:
        speedFrom=0
    speedFrom = int(speedFrom)

    speedTo = request.args.get('speedTo')
    if speedTo is None:
        speedTo=9999999
    speedTo = int(speedTo)

    list_database = client.init_languages
    list_collection = list_database.languages_collection
    # for each in list_collection.find({}):
    #     print(each)
    filter_task = list_collection.find({'forks': {'$gte': forksFrom, '$lte': forksTo},
                                        'stargazers_count': {'$gte': starsFrom, '$lte': starsTo},
                                        'size': {'$gte': sizeFrom, '$lte': sizeTo},
                                        'speed': {'$gte': speedFrom, '$lte': speedTo}},
                                       {'_id': 0, 'id': 1,
                                        'name': 1,
                                        'language': 1,
                                        'forks': 1,
                                        'stargazers_count': 1,#звёзды
                                        'size': 1,
                                        'speed': 1})
# тебе нужно видимо из каждого документа брать значения таких полей как
# 'forks', 'stargazers_count', 'size', 'speed' - четыре графика и 'language'-язык

    # json_docs = []
    # for doc in filter_task:
    #     print(doc)
    #     json_doc = json.dumps(doc, default=json_util.default)
    #     json_docs.append(json_doc)


    json_docs = []
    for doc in filter_task:
        json_docs.append(doc)

    with open('data_file.json', 'w') as write_file:
        json.dump({"data": json_docs}, write_file, indent=4)

    return jsonify({"data": json_docs})


@app.route("/")
def last_number_list():
    return render_template('index-basic.html')
	
@app.route("/step2")
def step2():
    return render_template('index-basic2.html')

    #return Response(json.dumps(extracted, default=json_util.default), status=200, mimetype='application/json')
    #last_numbers = list(random_numbers.find({"_id" : "lasts"}))
    #extracted = [d['value'] for d in last_numbers[0]['items']]



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.config['DEBUG'] = True
    app.run(host='127.0.0.1', port=port)

