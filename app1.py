from flask import Flask, request, jsonify
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


#get all tasks from mongodb database (Retrieve list of tasks)
@app.route('/getTask', methods=['GET'])
def getTask():
        myTask = mongo.db.myTask
        match = myTask.find({},{'_id':0})
        task = []
        for i in match:
            task.append(i)
        return jsonify(task)


#user write numeric id with url if id match user get a single task from mongodb database (Retrieve a task)
@app.route('/getSingleTask/<id>', methods=['GET'])
def getSingleTask(id):
        myTask = mongo.db.myTask
        match = myTask.find_one({'id':int(id)},{'_id':0})
        if match:
            return jsonify(match)
        return """
        <h2> ID not Found.</h2>
        """
        

#user post 4 fields (id,title,description,done) in jason dictionary format to create a new task
@app.route('/createTask', methods=['POST'])
def createTask():
    task = request.json
    myTask = mongo.db.myTask
    if task != None:
        if 'id' in task:
            match = myTask.find_one({'id':int(task['id'])})
            if match:
                return """
                <h2>"id" is already in use. "id" must be unique.</h2>
                """
            myTask.insert({'id':task['id'],'title':task['title'],'description':task['description'],'done':bool(task['done'])})
            return """
            <h2>Succesfully create a Task.</h2>
            """
    return """
    <h2> Wrong Text.</h2>
    """

#user post 4 fields (id,title,description,done) in jason dictionary format if id numeric and match user update other task fields 
@app.route('/updateTask', methods=['PUT'])
def updateTask():
    task = request.json
    myTask = mongo.db.myTask
    if task != None:
        if 'id' in task:
            match = myTask.find_one({'id':int(task['id'])})
            if match:
                myTask.delete_one({'id':int(id)})
            myTask.insert({'id':task['id'],'title':task['title'],'description':task['description'],'done':bool(task['done'])})
            return """
            <h2>Succesfully create a Task.</h2>
            """
    return """
    <h2> Wrong Text.</h2>
    """
        
    
#user write numeric id with url if id match user delete his task        
@app.route('/deleteTask/<id>', methods=['DELETE'])
def deleteTask(id):
    myTask = mongo.db.myTask
    match = myTask.find_one({'id':int(id)})
    if match:
        myTask.delete_one({'id':int(id)})
        
        return """
        <h2>Task succesfully deleted.</h2>
        """
    return """
    <h2>Wrong "id".</h2>
    """
    

app.run(debug=True)