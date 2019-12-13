from flask import Flask, render_template, redirect, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb+srv://umair:fabeha123@flaskapp-mteqh.mongodb.net/test?retryWrites=true&w=majority"

mongo = PyMongo(app)

task_list = [
    {
        "id": 101,
        "title": "repair laptop",
        "description": "need to find a good hardware engineer of computer", 
        "done": False
    },
    {
        "id": 102,
        "title": "ninja bootcamp",
        "description": "complete part 1 to show sir Zia before friday", 
        "done": False
    },
    {
        "id": 103,
        "title": "git exam wednesday",
        "description": "prepration of git exam", 
        "done": False
    },
    {
        "id": 104,
        "title": "ila exam monday",
        "description": "prepration of ILA exam", 
        "done": False
    }
]
#list of tasks posted to mongodb database
@app.route('/tasks',methods=['POST'])
def tasks():
    myTask = mongo.db.myTask
    myTask.insert(task_list)
    return """
    <h2>List of Tasks upload succesfully</h2>
    """
#user post only one field numeric id in jason dictionary format if id match user get his task
@app.route('/getTask', methods=['GET','POST'])
def getTask():
    task = dict(request.json)
    if task["id"] == int(task["id"]):
        myTask = mongo.db.myTask
        match = myTask.find_one({"id":task["id"]})
        if match:
            task = []
            task.append({'description': match['description'], 'title' : match['title'],'id': match['id'], 'done' : match['done']})
            return jsonify({"Succesfully get a Task" : task})
        else:
            return """
            <h2>Wrong "id"</h2>
            """
    else:
        return """
        <h2>Wrong "id". "id" must be numeric.</h2>
        """
#user post 4 fields (id,title,description,done) in jason dictionary format to create a new task
@app.route('/createTask', methods=['POST'])
def createTask():
    task = dict(request.json)
    if task["id"] == int(task["id"]) and task["title"] == str(task["title"]) and task["description"] == str(task["description"]) and task["done"] == bool(task["done"]):
        myTask = mongo.db.myTask
        match = myTask.find_one({"id":task["id"]})
        if match:
            return """
            <h2>"id" is already in use. "id" must be unique.</h2>
            """
        else:
            myTask.insert_one(task)
            return """
            <h2>Succesfully create a Task.</h2>
            """
    else:
        return """
        <h2>Wrong syntax. "id" must be numeric. "title" and "description" must be text. "done" must be true or false.</h2>
        """
#user post 4 fields (id,title,description,done) in jason dictionary format if id numeric and match user update other task fields 
@app.route('/updateTask', methods=['PUT'])
def updateTask():
    task = dict(request.json)
    task = dict(request.json)
    if task["id"] == int(task["id"]) and task["title"] == str(task["title"]) and task["description"] == str(task["description"]) and task["done"] == bool(task["done"]):
        myTask = mongo.db.myTask
        match = myTask.find_one({"id":task["id"]})
        if match:
            myTask.delete_one({"id":task["id"]})
            myTask.insert_one(task)
            return """
            <h2>Succesfully update a Task.</h2>
            """
        else:
            return """
            <h2>Wrong "id".</h2>
            """
    else:
        return """
        <h2>Wrong syntax. "id" must be numeric. "title" and "description" must be text. "done" must be true or false.</h2>
        """
#user post only one field numeric id in jason dictionary format if id match user delete his task        
@app.route('/deleteTask', methods=['POST'])
def deleteTask():
    task = dict(request.json)
    if task["id"] == int(task["id"]):
        myTask = mongo.db.myTask
        match = myTask.find_one({"id":task["id"]})
        if match:
            myTask.delete_one({"id":task["id"]})
            return """
            <h2>Task succesfully deleted.</h2>
            """
        else:
            return """
            <h2>Wrong "id".</h2>
            """
    else:
        """
        <h2>Wrong syntax. "id" must be numeric.</h2>
        """

app.run(debug=True)