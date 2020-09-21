from flask import Flask, jsonify, abort, make_response, request
import pymongo
import json
from bson import json_util



app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["todos"]

mycol = mydb["todoData"]


mydict = { "id": 3, "title": "Titletitle", "description": "dlkfjghn" }

#x = mycol.insert_one(mydict)

for x in mycol.find():
  print(x)


#REST GET = find all
@app.route('/todo/api/v1.0/tasks/', methods=['GET'])
def get_tasks():
    tasks = mycol.find()
    json_docs = [json.dumps(doc, default=json_util.default) for doc in tasks]
    return jsonify({"tasks": json_docs})

#REST GET = find by id
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    myquery = {"id": task_id}
    tasks = mycol.find(myquery)
    json_docs = [json.dumps(doc, default=json_util.default) for doc in tasks]
    return jsonify({"tasks": json_docs})

#REST POST = Create new
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

#REST PUT = UPDATE
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    print(request.json)
    list = mycol.find({"id": task_id})
    tasks = [json.dumps(doc, default=json_util.default) for doc in list]

    if len(tasks) == 0:
        print("------None found")
        abort(404)
    if not request.json:
        print("------No Data")
        abort(400)
        #and type(request.json['title']) != unicode
    if 'title' in request.json:
        print("------Title Issue")
        #abort(400)
    if 'description' in request.json:
        print("------Desc Issue")
        #abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        print("------Done Issue")
        #abort(400)


    #request.json.get('title', tasks[0]['title']).Title
    print(type(tasks))
    print(tasks)
    print(type(tasks[0]))
    print(tasks[0])

    y = json.loads(tasks[0])
    y["title"] =  "newTitle"
    print(y)
    #["description"] = "TEST"
    #request.json.get("description", tasks[0]['description'])
    #tasks[0]['done'] = request.json.get('done', tasks[0]['done'])

    myquery = {"id": task_id}
    newvalues = { "$set": jsonify(tasks[0])}

    mycol.update_one(myquery, newvalues)

    return jsonify({'task': tasks[0]})

#REST DELETE
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    myquery = {"id": task_id}
    mycol.delete_one(myquery)
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Gibts nichts zu holen hier'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
